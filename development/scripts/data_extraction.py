import pymupdf
import re
from rapidfuzz import fuzz, process
import os
import json

# Open the PDF and read the table of contents
doc = pymupdf.open("a guide to modern cookery.pdf")
toc_pages = [doc[20], doc[21]]
toc_page_texts = []

for page in toc_pages:
    text = page.get_text()
    toc_page_texts.append(text)
    
chapters = {}

for text in toc_page_texts:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i > 3:
            if i%2 == 1:
                # the title is the first words of the line 
                # followed by some amount of "."
                # the page number is at the end
                split_text = line.split(".")
                title = split_text[0]
                page_num = split_text[-1]
                chapters[title] = page_num 
            
# fixing some of the mistakes from the OCR manually
chapters['FONDS  DE  CUISINE  '] = 1
chapters['THE  LEADING  WARM   SAUCES     '] = 15
chapters['THE  COURT-BOUILLONS  AND  THE  MARINADES  '] = 64
correct_titles = [
    'THE  ELEMENTARY  PREPARATIONS  ',
    'GARNISHING  PREPARATIONS   FOR  RELEVES  AND   ENTREES  ',
    'LEADING  CULINARY  OPERATIONS  ',
    "HORS-D'OEUVRES      ",
    "RELEVES  AND  ENTREES  OF  BUTCHER'S  MEAT  ",
    "RELEVES  AND  ENTREES  OF  POULTRY  AND  GAME    "  
]
incorrect_titles = [
    '\J/:  ELEMENTARY  PREPARATIONS  ',
    'GARNISHING  PREPARATIONS   FOR  RELEVis  AND   ENTR]£eS  ',
    'U^DING  CULINARY  OPERATIONS  ',
    "HORS-D'CEUVRES      ",
    "RELEVilS  AND  ENTRIES  OF  BUTCHER'S  MEAT  ",
    "RELEVES  AND  ENTRIES  OF  POULTRY  AND  GAME    " 
]
for i in range(len(correct_titles)):
    chapters[correct_titles[i]] = chapters[incorrect_titles[i]]
    del chapters[incorrect_titles[i]]

# Sort back into order and correct the page numbers to match the PDF page numbers
chapters = dict(sorted(chapters.items(), key=lambda item: int(item[1])))
for chapter in chapters:
    chapters[chapter] = int(chapters[chapter])+26  # first page is 27, and -1 for zero indexing

# iterate through each chapter's recipes and extract them into JSONs
titles = list(chapters.keys())
page_nums = list(chapters.values())
all_recipes = {}

n = 0
for i in range(0, len(page_nums)):
    pages = []
    recipes = []
    if i+1 == len(page_nums):
        chapter_range = [page_nums[i], len(doc)]
    else:
        chapter_range = [page_nums[i], page_nums[i+1]]
    print(f"The current chapter range is: {chapter_range[0]} to {chapter_range[1]}.")
    
    # filtering out the title and chapter title lines
    target_phrases = ["GUIDE TO MODERN COOKERY", titles[n]]
    for j in range(chapter_range[0], chapter_range[1]):
        page = doc[j]
        text = page.get_text()
        lines = text.splitlines()
        filtered_lines = [
            line for line in lines
            if not any(fuzz.partial_ratio(line.strip(), phrase) > 80 for phrase in target_phrases)
        ]
        pages.append("\n".join(filtered_lines))
    chapter_text = "\n".join(pages)

    # extracting recipes
    # extract number and title
    recipe_pattern = re.compile(
        r'(?P<header>[A-Za-z0-9]{1,4}—\s+.+?)(?=\n[A-Za-z0-9]{1,4}—|\Z)',
    re.DOTALL)  # 1 to 4 character identifiers,the em dash, spaces, look ahead to stop capturing when another identifier is found

    for block in recipe_pattern.finditer(chapter_text):
        block_text = block.group(0) # extract whole match
        current_recipe = {}

        # extract title and id
        header_patter = re.compile(
            r'^(?P<id>[A-Za-z0-9]{1,4})—(?P<title>.*)$',
            re.MULTILINE
        )
        header_match = header_patter.search(block_text)
        if header_match:
            current_recipe["recipe_id"] = header_match.group("id")
            current_title = header_match.group("title").strip()
            # extract everything until the next recipe match and add to current_recipe as "instructions"
            current_instructions = block_text[header_match.end():].strip().replace("\n","")
            
            # remove the extra spaces and swap '^' with 'e' 
            current_title = current_title.replace('^', 'e')
            current_instructions = current_instructions.replace('^', 'e')
            current_title = re.sub(r'\s+', ' ', current_title).strip()
            current_instructions = re.sub(r'\s+', ' ', current_instructions).strip()

            current_recipe['title'] = current_title
            current_recipe['instructions'] = current_instructions
        else:
            # if no header is found, just store everything as instructions
            current_instructions = block_text.strip().replace("\n", "")
            current_instructions = current_instructions.replace('^', 'e')
            current_instructions = re.sub(r'\s+', ' ', current_instructions).strip()
            current_recipe["instructions"] = current_instructions

        # add to list of recipes for this chapter
        recipes.append(current_recipe)
    
    # add list of this chapter's recipes to the dictionary of recipes by chapter
    all_recipes[titles[n]] = recipes 
    n += 1

output_dir = "json_chapters"
os.makedirs(output_dir, exist_ok=True)

for title in titles:
    recipes = all_recipes[title]
    filename = f"{title}.json"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding='utf-8') as f:
                json.dump(recipes, f, indent=4, ensure_ascii=False)
