import streamlit as st
from models import bot
import pandas as pd
from models import knowledgegraphcharacters
from models import contradictionDetector


st.set_page_config(layout="wide")


df = pd.DataFrame({
    "Character": ["Harry Potter", "Hermione Granger", "Ron Weasley", "Severus Snape", "Albus Dumbledore"],
    "Personality": [
        "You are Harry Potter, the famous young wizard known for your bravery, loyalty, and strong sense of justice.",
        "You are Hermione Granger, a highly intelligent and resourceful witch, known for your keen intellect and loyalty.",
        "You are Ron Weasley, the loyal and courageous friend of Harry Potter, always standing by your friends.",
        "You are Severus Snape, a complex and mysterious wizard, known for your harsh demeanor and hidden loyalty.",
        "You are Albus Dumbledore, a wise and powerful wizard, known for your deep knowledge and compassion."
    ]
})

house_themes = {
    "Gryffindor": {"primaryColor": "#FFD700", "backgroundColor": "#7F0909", "textColor": "#FFD700"},
    "Ravenclaw": {"primaryColor": "#0077CC", "backgroundColor": "#0E1A40", "textColor": "#A6D1FF"},
    "Hufflepuff": {"primaryColor": "#FFF200", "backgroundColor": "#1C1C1C", "textColor": "#FFF200"},
    "Slytherin": {"primaryColor": "#2ECC71", "backgroundColor": "#14532d", "textColor": "#CFFFE4"}
}

selected_house = st.sidebar.selectbox("Choose Your House 🏰", list(house_themes.keys()))
theme = house_themes[selected_house]

st.markdown(f"""
    <style>
        html, body, .stApp {{
            background-color: {theme['backgroundColor']} !important;
            color: {theme['textColor']} !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {theme['primaryColor']} !important;
        }}
        .stButton>button {{
            background-color: {theme['primaryColor']} !important;
            color: black !important;
            font-weight: bold;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {theme['primaryColor']} !important;
            color: black !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("🌌 Fictional Universe KIT")

tabs = st.tabs([
    "👤 Characters", "📜 Consistency Checker", "🌍 Rules & Lore", "⏳ Timelines", "⚙️ Technologies", "🧩 Magic/Systems"
])

with tabs[0]:
    st.header("👤 Character Database")
    character_name = st.text_input("Search Character Name", key="character_name")
    
    if character_name:
        if character_name.title() in df["Character"].values:
            character_description = df[df["Character"] == character_name]["Personality"].values[0]
            st.markdown(f"**Character:** {character_name}")
            st.text_area("Traits & Description", value=character_description, height=100, disabled=True)
            
            user_input = st.text_input(f"Talk to {character_name}", key="user_input")
            
            if user_input:
                response = bot.generate_character_response(character_name, user_input, character_description)
                st.markdown(f"**{character_name}:** {response}")
        else:
            st.warning("Character not found. Please enter a valid character name.")

with tabs[1]:
    st.header("Consistency checker")
    vector_database = contradictionDetector.initialize_database()
    inp = st.text_input("Enter prompt", key="consistency prompy")
    if inp:
        if vector_database is not None and vector_database.count() > 0:
            with st.spinner("Checking consistency..."):
                relevant_chunks = contradictionDetector.search_chroma(vector_database, inp)
                context = "\n".join(relevant_chunks)
                final_prompt = contradictionDetector.prompt_template.format(question=inp)
                consistency_result = contradictionDetector.generate_answer(final_prompt, context, contradictionDetector.generation_model_name)
            st.subheader("Consistency Check Result:")
            st.write(consistency_result)
        else:
            st.warning("The Chroma database is not initialized. Please wait for the initialization to complete.")

            
with tabs[2]:
    st.header("📜 Knowledge Graphs")
    st.title("🧙‍♂️ Harry Potter Character Graph")

    st.markdown("""
    Step into the wizarding web of Hogwarts' finest.  
    This graph shows who's friends, foes, or family — in true magical fashion! 
    """)

    st.subheader("Select the type of graph to display:")
    graph_type = st.selectbox(
        "Choose the graph to display:",
        options=["Character Graph", "Loyalty Graph","Location Graph", "Individual Character"]
    )
    if graph_type == "Character Graph":
        st.subheader("Select the number of top characters to display:")
        
        top_n = st.slider(
            "Choose the number of top characters:",
            min_value=20,
            max_value=100,
            value=20, 
            step=10, 
            format="%d" 
        )
        fig = knowledgegraphcharacters.plot_character_graph(top_n=top_n, house=selected_house)
        st.pyplot(fig)
    
    elif graph_type == "Loyalty Graph":
        fig = knowledgegraphcharacters.plot_loyalty_graph(house=selected_house)
        st.pyplot(fig)

    elif graph_type == "Location Graph":
        fig = knowledgegraphcharacters.plot_location_graph(house=selected_house)
        st.pyplot(fig)

    elif graph_type == "Individual Character":
        character_name = st.text_input("Enter a character name (e.g., Harry Potter):")
        graph_mode = st.radio("Select graph type", ["Relationship", "Loyalty"])
        if character_name:
            if graph_mode == "Relationship":
                fig = knowledgegraphcharacters.plot_character_relationships(character=character_name, house=selected_house)
            else:
                fig = knowledgegraphcharacters.plot_character_loyalties(character=character_name, house=selected_house)
            if fig:
                st.pyplot(fig)
        else:
            st.warning("Not present for this graph")


with tabs[3]:
    st.header("⏳ Timeline ")
    top_n = st.slider(
        "Choose the Book till timeline:",
        min_value=1,
        max_value=7,
        value=1, 
        step=1, 
        format="%d" 
    )
    timelineof = st.radio("Select graph type", ["Overall", "Character"])
    if timelineof == "Overall" : 
        st.warning("In progress")
    elif timelineof == "Character" :
        st.warning("In progress")

with tabs[4]:
    st.header("⚙️ Potions")
    tech_name = st.text_input("Potions Name")
    st.text_area("Functionality / Description")
    st.text_input("Creator / Origin")
    st.text_area("Appears in")

with tabs[5]:
    st.header("🧩 Magic, Power Systems, or Special Mechanics")
    system_name = st.text_input("Name of System (e.g, Mana, Chi, Force)")
    st.text_area("How It Works")
    st.text_input("Limitations or Rules")
    st.text_input("Who Can Use It")
