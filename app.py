import streamlit as st

house_themes = {
    "Gryffindor": {
        "primaryColor": "#FFD700",
        "backgroundColor": "#7F0909",
        "textColor": "#FFD700",
    },
    "Ravenclaw": {
        "primaryColor": "#0077CC",
        "backgroundColor": "#0E1A40",
        "textColor": "#A6D1FF",
    },
    "Hufflepuff": {
        "primaryColor": "#FFF200",
        "backgroundColor": "#1C1C1C",
        "textColor": "#FFF200",
    },
    "Slytherin": {
        "primaryColor": "#2ECC71",
        "backgroundColor": "#14532d",
        "textColor": "#CFFFE4",
    }
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

st.title("🌌 Fictional Universe World Model")

tabs = st.tabs([
    "👤 Characters", "🌍 Locations", "📜 Rules & Lore",
    "⏳ Timelines", "⚙️ Technologies", "🧩 Magic/Systems"
])

with tabs[0]:
    st.header("👤 Character Database")
    character_name = st.text_input("Search Character Name")
    if character_name:
        st.markdown(f"**Character:** {character_name}")
        st.text_input("Affiliation / Group")
        st.text_area("Traits & Description")
        st.text_area("Key Events or Arcs")

with tabs[1]:
    st.header("🌍 Location Index")
    location_name = st.text_input("Search Location Name")
    if location_name:
        st.markdown(f"**Location:** {location_name}")
        st.text_area("Description / Lore")
        st.text_input("Region / Planet / Realm")
        st.text_input("Notable Events")

with tabs[2]:
    st.header("📜 World Rules & Lore")
    rule = st.text_area("Check for a World Rule or Lore Element")
    st.selectbox("Category", ["Magic", "Technology", "Government", "History", "Other"])
    if st.button("Add Rule"):
        st.success("Rule saved (not really, this is just a prototype).")

with tabs[3]:
    st.header("⏳ Timeline Builder")
    st.text_input("Event Name")
    st.date_input("Date / Time Period (if applicable)")
    st.text_area("Event Description")
    st.info("Coming soon: Visual timeline plot and consistency validation.")

with tabs[4]:
    st.header("⚙️ Potions")
    tech_name = st.text_input("Potions Name")
    st.text_area("Functionality / Description")
    st.text_input("Creator / Origin")
    st.text_area("Appears in")

with tabs[5]:
    st.header("🧩 Magic, Power Systems, or Special Mechanics")
    system_name = st.text_input("Name of System (e.g., Mana, Chi, Force)")
    st.text_area("How It Works")
    st.text_input("Limitations or Rules")
    st.text_input("Who Can Use It")
