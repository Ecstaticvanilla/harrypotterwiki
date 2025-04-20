import os
from dotenv import load_dotenv
import chromadb
import google.generativeai as genai
import streamlit as st
from sentence_transformers import SentenceTransformer

try:
    api_key = st.secrets["gemini_apikey"]
    genai.configure(api_key=api_key)
except KeyError:
    print("Gemini API key not found in Streamlit secrets. Ensure it's set up correctly.")

embedding_model_name = "all-MiniLM-L6-v2"
generation_model_name = "gemini-1.5-pro"

BOOK_FILE_PATHS = [
    "data/books/harry-potter-1.txt",
    "data/books/harry-potter-2.txt",
    "data/books/harry-potter-3.txt",
    "data/books/harry-potter-4.txt",
    "data/books/harry-potter-5.txt",
    "data/books/harry-potter-6.txt",
    "data/books/harry-potter-7.txt",
]
CHROMA_DB_PATH = "harry_potter_chroma_db"
COLLECTION_NAME = "harry_potter_lore"

def load_books(book_paths):
    """Loads text from book files."""
    all_texts = []
    for path in book_paths:
        with open(path, "r", encoding="utf-8") as f:
            all_texts.append(f.read())
    return all_texts

def chunk_text(texts, chunk_size=1000, chunk_overlap=100):
    """Splits text into smaller chunks."""
    chunks = []
    for text in texts:
        for i in range(0, len(text), chunk_size - chunk_overlap):
            end = i + chunk_size
            chunk = text[i:end]
            chunks.append(chunk)
    return chunks

def get_chroma_collection():
    """Gets the Chroma collection. Creates it if it doesn't exist."""
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection

def initialize_database():
    """Initializes the Chroma database if it doesn't exist."""
    collection = get_chroma_collection()
    if collection.count() == 0:
        st.info("Initializing Chroma database. This might take a few minutes...")
        book_texts = load_books(BOOK_FILE_PATHS)
        knowledge_base_chunks = chunk_text(book_texts)
        embedding_model = SentenceTransformer(embedding_model_name)
        embeddings = embedding_model.encode(knowledge_base_chunks)
        ids = [f"chunk_{i}" for i in range(len(knowledge_base_chunks))]
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=knowledge_base_chunks
        )
        st.success("Chroma database initialized!")
    else:
        st.write("✨")
    return collection

@st.cache_resource
def get_vector_database():
    """Loads the existing Chroma database."""
    return get_chroma_collection()

def search_chroma(collection, query, n_results=3):
    """Searches Chroma for relevant documents."""
    embedding_model = SentenceTransformer(embedding_model_name)
    embedding = embedding_model.encode([query])[0]
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        include=["documents"]
    )
    return results["documents"][0]

def generate_answer(prompt, context, model_name):
    """Generates an answer using Gemini."""
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(f"{prompt}\n\nContext:\n{context}")
    return response.text

prompt_template = """Use the following context from the Harry Potter books to determine if the user's prompt is consistent with established facts. If the prompt is inconsistent, explain why and quote the relevant information from the context if possible. Give suggestions which the User input cn change to make it more consistent. If the prompt is consistent, simply state "Consistent."

User Prompt: {question}
"""
#--------------------------------------------------------------------------
def suggest_plot_points(fanfic_text: str, n_context: int = 5) -> str:
    """
    Suggests possible plot continuations for a half-written fanfic using Harry Potter canon.
    
    Args:
        fanfic_text (str): The partial fanfic input.
        n_context (int): Number of canon-relevant chunks to retrieve from ChromaDB.
    
    Returns:
        str: Gemini-generated plot point suggestions.
    """
    collection = get_vector_database()
    context_chunks = search_chroma(collection, fanfic_text, n_results=n_context)
    context = "\n\n---\n\n".join(context_chunks)
    prompt = f"""You are an expert fanfiction assistant with deep knowledge of the Harry Potter universe.

    The user is writing a fanfic, but it's currently unfinished. Based on the fanfic so far and some relevant canonical context, suggest 3–5 plot directions they could continue with.
    
    Ensure your suggestions make sense within Harry Potter lore and build logically on what’s been written.
    
    Fanfic so far:
    {fanfic_text}
    
    Context from Canon:
    {context}
    Plot Continuation Suggestions:"""
    return generate_answer(prompt, context="", model_name=generation_model_name)
