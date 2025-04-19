import google.generativeai as genai
import streamlit as st

api_key = st.secrets["gemini_apikey"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

def generate_character_response(character_name, user_input, character_description):
    prompt = f"""
    You are {character_name}, the character with the following traits:
    {character_description}

    Stay in character in every response. Don't reveal you're an AI.

    User: {user_input}
    Character:"""
    
    response = model.generate_content(prompt)
    return response.text.strip()
