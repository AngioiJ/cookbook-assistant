# Recipe Assistant Project Plan

### Loose Plan
1) Data Extraction from PDFs of Cookbooks 
- extract key metadata such as ingredients, techniques, and flavor profiles

2) Implement Retrieval Augmented Generation (RAG). 
- store the structured recipes in a vector database
- use embedding models to index and retrieve relevant recipes based on user queries
- pass retrieved data to an LLM to generate the response

3) Implement the following prompts:
- "What can I cook with X?"
- "How do I prepare Y?"
- "What is Z technique?"
- "Pairing suggestions?" - stretch goal, this could  lowkey be its own model

4) Frontend Options
- Build a small chatbot interface using React - FastAPI
- Create a CLI or Jupyter Notebook demo
- Streamlit or Gradio for a lightweight web interface



## Part One: Data Extraction
Steps:
1. Load and iterate through the PDFs
2. Identify recipe sections using text patterns, headers, and formatting
3. Store extracted data in a structured format (JSON, CSV, etc)
### Step One: Text Extraction and Data Structuring
Methods:
    - `PyMuPDF` or pdf plumber for extracting structured text
    - Regex Python module
    - `rapidfuzz` fuzzy matching for cleaning lines while allowing for typos
    - 
Chose `PyMuPDF` since OCR was already performed on the PDF. Added further cleaning steps to handle OCR issues. 

### Step Two: Data Structuring
Method: 
    - Parse extracted text using `spaCy` or `NLTK`.
    - Use `Named Entity Recognition (NER)` for metadata extraction.
Data to Extract:
- *Technique* ("sous-vide", "roast", "saute", etc.)
- *Ingredients list* ("butter", "thyme", etc.)
- *Amounts* ("200g", "1 Tablespoon", "2 cups", etc.)
- *Time steps or target threshold*

### Step Three: Data Storing
Method: A vector database 


## Part Two: Implementing RAG
Retrieval Model: Offline embedding model through Ollama
- maybe `text-embedding-ada-002`
- optimize using query expansion before retrieval?
LLM Integration: Pass retrieved data to an offline language model through Ollama to generate responses.

Key Prompts:
- "What can I cook with X?"
- "How do I prepare Y?"
- "What is Z technique?"


## Part Three: Frontend and UI
Method: Use Gradio to make a simple chatbot interface.
- User input via text box for queries.
- LLM response via formatted text display for the generated answer.


