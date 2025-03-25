# An Interactive Guide to Modern Cookery


### Introduction


### Setup Instructions



### A Guide To What's Been Done
1) Data Extraction from PDFs of Cookbooks 
- Extracted recipes and stored them in a structured manner. 
    - Extracted text using `PyMuPDF`.
    - Identified recipes and key information using Python's Regular Expression module `re`.
    - Stored recipes using JSON format.
- See `data extraction.ipynb`.

2) Implement Retrieval Augmented Generation (RAG). 
- Stored the structured recipes in a vector database.
    - Used `ChromaDB`.
- Used embedding models to index and retrieve relevant recipes based on user queries.
    - Embeddings computed via `mxbai-embed-large:latest` and `Ollama`.
- Used retrieved data to and an LLM to generate responses.
    - Responses generated via `llama3:latest`.
- See `rag.ipynb`.

3) Frontend and UI
- Built a basic chat interface using `Gradio`.


### Future plans: 
- Typo fixes for the OCR of the original document.
    - Will use SymSpell over TextBlob due to multilingual text due to various french loan words present.
- NER on the recipes for filtering based on ingredients and methods.
- Compare different embedding models.
- Compare different LLM models.
- Evaluate the necessity of a chunking method for longer recipes.
- Add a chat history for developing recipes
- Add a feature for users to save recipes they've developed.
- Add a feature to load saved recipes for further development or modification.
- Find other public domain cookbooks for other cuisines (e.g. if Marcella Hazan's "Essentials of Italian Cooking" were public domain).
