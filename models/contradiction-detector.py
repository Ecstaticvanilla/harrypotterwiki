import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader  
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain.embeddings import GooglePalmEmbeddings  
from langchain.vectorstores import Chroma  
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI  


import streamlit as st

api_key = st.secrets["gemini_apikey"]


def load_and_chunk_books(book_paths):
    """Loads text from book files and chunks it."""
    all_texts = []
    for path in book_paths:
        loader = TextLoader(path)
        documents = loader.load()
        all_texts.extend(documents)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_texts)
    return chunks

book_file_paths = [
    "harry_potter_book1.txt",
    "harry_potter_book2.txt",
]
knowledge_base_chunks = load_and_chunk_books(book_file_paths)

CHROMA_DB_PATH = "harry_potter_chroma_db" 

def get_vector_store(chunks):
    embeddings = GooglePalmEmbeddings(google_api_key=api_key)
    if os.path.exists(CHROMA_DB_PATH):
        print("Loading existing Chroma database...")
        vector_store = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    else:
        print("Creating and persisting Chroma database...")
        vector_store = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DB_PATH)
        vector_store.persist()
    return vector_store

vector_database = get_vector_store(knowledge_base_chunks)


prompt_template = """Use the following pieces of context from the Harry Potter books to determine if the user's prompt is consistent with established facts. If the prompt is inconsistent, explain why and quote the relevant information from the context if possible. If the prompt is consistent, simply state "Consistent."

Context:
{context}

User Prompt: {question}
Answer: """

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


def setup_rag_chain_gemini(vector_store):
    """Sets up the RetrievalQA chain using Gemini for generation."""
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}), 
        chain_type_kwargs={"prompt": PROMPT}
    )
    return rag_chain

rag_model = setup_rag_chain_gemini(vector_database)


def check_harry_potter_consistency(prompt):
    """Checks if a given prompt is consistent with Harry Potter lore using the RAG model with Gemini."""
    result = rag_model({"query": prompt})
    return result["result"]


if __name__ == "__main__":
    inconsistent_prompt = "Harry becomes a professional Quidditch player for Slytherin after Hogwarts."
    consistency_check_result_inconsistent = check_harry_potter_consistency(inconsistent_prompt)
    print(f"Prompt: {inconsistent_prompt}\nResult: {consistency_check_result_inconsistent}\n")

    consistent_prompt = "Hermione works in the Ministry of Magic after the war."
    consistency_check_result_consistent = check_harry_potter_consistency(consistent_prompt)
    print(f"Prompt: {consistent_prompt}\nResult: {consistency_check_result_consistent}\n")

    another_inconsistent_prompt = "Dumbledore taught Potions at Hogwarts."
    consistency_check_result_another_inconsistent = check_harry_potter_consistency(another_inconsistent_prompt)
    print(f"Prompt: {another_inconsistent_prompt}\nResult: {consistency_check_result_another_inconsistent}\n")