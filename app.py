import streamlit as st

st.set_page_config(page_title="Universe Consistency Kit", layout="wide")

st.title("🌌 Fictional Universe World Model")

# Top-level tabs
tabs = st.tabs(["👤 Characters", "🌍 Locations", "📜 Rules & Lore", "⏳ Timelines", "⚙️ Technologies", "🧩 Magic/Systems"])

# ----------------------------
with tabs[0]:  # Characters
    st.header("👤 Character Database")
    character_name = st.text_input("Search or Add Character Name")
    if character_name:
        st.markdown(f"**Character:** {character_name}")
        st.text_input("Affiliation / Group")
        st.text_area("Traits & Description")
        st.text_area("Key Events or Arcs")

# ----------------------------
with tabs[1]:  # Locations
    st.header("🌍 Location Index")
    location_name = st.text_input("Search or Add Location Name")
    if location_name:
        st.markdown(f"**Location:** {location_name}")
        st.text_area("Description / Lore")
        st.text_input("Region / Planet / Realm")
        st.text_input("Notable Events")

# ----------------------------
with tabs[2]:  # Rules & Lore
    st.header("📜 World Rules & Lore")
    rule = st.text_area("Enter a World Rule or Lore Element")
    st.selectbox("Category", ["Magic", "Technology", "Government", "History", "Other"])
    if st.button("Add Rule"):
        st.success("Rule saved (not really, this is just a prototype).")

# ----------------------------
with tabs[3]:  # Timelines
    st.header("⏳ Timeline Builder")
    st.text_input("Event Name")
    st.date_input("Date / Time Period (if applicable)")
    st.text_area("Event Description")
    st.info("Coming soon: Visual timeline plot and consistency validation.")

# ----------------------------
with tabs[4]:  # Technologies
    st.header("⚙️ Technologies / Artifacts")
    tech_name = st.text_input("Tech or Artifact Name")
    st.text_area("Functionality / Description")
    st.text_input("Creator / Origin")
    st.text_area("Appears in")

# ----------------------------
with tabs[5]:  # Magic/Systems
    st.header("🧩 Magic, Power Systems, or Special Mechanics")
    system_name = st.text_input("Name of System (e.g., Mana, Chi, Force)")
    st.text_area("How It Works")
    st.text_input("Limitations or Rules")
    st.text_input("Who Can Use It")

