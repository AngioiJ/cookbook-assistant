import ollama
import chromadb
import gradio as gr

# Number of recipes to look at to respond to a user's prompt. 
RECIPE_CONTEXT_LENGTH = 5
# Chosen Ollama model
OLLAMA_MODEL = "llama3"

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="recipes")


def rag_query(input: str):
    embed_response = ollama.embed(
        model="mxbai-embed-large",
        input=input
    )
    results = collection.query(
        query_embeddings=[embed_response["embeddings"][0]],
        n_results=RECIPE_CONTEXT_LENGTH
    )

    context = results['documents'][0]
    formatted_context = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(context)])

    return formatted_context


def generate_response(prompt: str):
    context = rag_query(prompt)

    llm_response = ollama.generate(
        model=OLLAMA_MODEL,
        prompt=f"Using these recipes: {context}. Respond to this prompt using one or some of the techniques contained: {prompt}"
    )

    return llm_response['response']


iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Ask a recipe question here..."),
    outputs="text",
    title="An Interactive Guide to Modern Cookery",
    description="Receive guidance on haute cuisine from an interactive version of Auguste Escoffier's Guide to  Modern Cookery."
)


if __name__ == "__main__":
    iface.launch()