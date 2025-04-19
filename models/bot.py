import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["gemini_apikey"])
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

st.title("🎭 Character Chatbot with Gemini")

character_description = st.text_area(
    "Describe your character", 
    placeholder="E.g., You are 'Zara', a witty and sarcastic hacker who never follows rules..."
)

if "history" not in st.session_state:
    st.session_state.history = []

if "submit" not in st.session_state:
    st.session_state.submit = False

def submit():
    st.session_state.submit = True

user_input = st.text_input("You:", key="user_input", on_change=submit)

if st.session_state.submit and user_input and character_description:
    full_prompt = f"""
Act as the following character: 
{character_description}

Stay in character in every response. Don't reveal you're an AI.

User: {user_input}
Character:"""

    response = model.generate_content(full_prompt)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Character", response.text.strip()))
    st.session_state.submit = False
    st.rerun()

for role, msg in st.session_state.history:
    st.markdown(f"**{role}:** {msg}")
