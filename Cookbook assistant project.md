# Recipe Assistant Project Plan

### A Guide To What's Been Done
1) Data Extraction from PDFs of Cookbooks 
- Extract recipes and store them in a structured manner. 
    - Extracted text using `PyMuPDF`
    - Identified recipes and key information using Python's Regular Expression module `re`
    - Stored recipes using JSON format
- Optionally to improve responses: 
    - Try extracting various metadata about each recipe using Named Entity Recognition
    - Compare embedding models
    - Compare LLM models
    - Try chunking longer recipes and comparing length thresholds

2) Implement Retrieval Augmented Generation (RAG). 
- store the structured recipes in a vector database
    - Used ChromaDB
- use embedding models to index and retrieve relevant recipes based on user queries
    - Embeddings computed via `mxbai-embed-large:latest`
- pass retrieved data to an LLM to generate the response
    - Responses generated via `llama3:latest`

3) Implement the following prompts:
- "What can I cook with X?"
- "How do I prepare Y?"
- "What is Z technique?"
- "Pairing suggestions?" - stretch goal, this could  lowkey be its own model

4) Frontend and UI
- Build a small chatbot interface using Gradio
- Create a CLI or Jupyter Notebook demo


Future work: 
- NER on the recipes.
- Compare different embedding models.


Note: I would prefer to use Marcella Hazan's cookbook The Essentials of Italian Cooking for this application, but it's not public domain. For my personal use, I will expand this project to include it along with various books from Marco Pierre White, Thomas Keller, and etc.
