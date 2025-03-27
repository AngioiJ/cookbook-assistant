import json
import os 
import ollama
import chromadb

# load the recipe JSONs as `documents`
json_recipe_files = [f for f in os.listdir("json_chapters")]
json_recipe_files = [os.path.join("json_chapters",file) for file in json_recipe_files]
documents = []
ids =[]

for file in json_recipe_files:
    with open(file, "r") as f:
        data = json.load(f)

        for recipe in data:
            text = f"Title: {recipe['title']} \n Instructions: {recipe['instructions']}"
            documents.append(text)
            ids.append(recipe['recipe_id'])

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="recipes")

# store each document in a vector embedding database
i = 0
for recipe_id, recipe in zip(ids, documents):
  if i % 100 == 0:
    print(f"Embedding recipe: {i+1}.")
  response = ollama.embed(model="mxbai-embed-large:latest", input=recipe)
  embeddings = response["embeddings"]
  # break
  collection.add(
    ids=[str(recipe_id)],  # use the recipe ID from the JSON instead
    embeddings=embeddings[0],
    documents=[recipe]
    # can add recipe metadata here such as ingredients and the chapter title
  )
  i += 1