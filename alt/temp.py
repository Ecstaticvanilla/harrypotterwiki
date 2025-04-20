import streamlit as st
import pandas as pd
import spacy
from sklearn.preprocessing import LabelEncoder

# ========== Load CSV Data ==========
@st.cache_data
def load_data():
    return pd.read_csv("final_cleaned_character_events.csv")

df = load_data()

# ========== Load spaCy Model ==========
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

# ========== Step 1: NER Fallback (if core_entities missing or empty) ==========
def extract_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'GPE', 'ORG', 'EVENT']]

if 'core_entities' not in df.columns or df['core_entities'].isnull().all():
    df['core_entities'] = df['event_summary'].apply(extract_entities)

# ========== Step 2: Semantic Event Extraction ==========
def extract_semantic_relation(text):
    doc = nlp(text)
    relations = []
    for token in doc:
        if token.dep_ == "ROOT":
            subj = [w.text for w in token.lefts if w.dep_ == "nsubj"]
            obj = [w.text for w in token.rights if w.dep_ in ["dobj", "attr", "prep"]]
            if subj and obj:
                relations.append((subj[0], token.text, obj[0]))
    return relations

df['semantic_events'] = df['event_summary'].apply(extract_semantic_relation)

# ========== Step 3: Detect Relative Time Cues ==========
def detect_relative_time(summary):
    cues = ["yesterday", "next day", "that night", "soon after", "an hour later", "a week ago", "this morning"]
    for cue in cues:
        if cue in summary.lower():
            return cue
    return None

df['relative_time_cue'] = df['event_summary'].apply(detect_relative_time)

# ========== Step 4: Intelligent Scoring ==========
event_type_weights = {
    'death': 5, 'battle': 4, 'magic': 3, 'discovery': 3, 'emotional': 2,
    'dialogue': 1, 'movement': 1, 'other': 1
}

entity_weights = {
    'Harry Potter': 5, 'Harry': 5, 'Voldemort': 5, 'Ron': 4, 'Hermione': 4,
    'Dobby': 3, 'Dumbledore': 4, 'Hogwarts': 3, 'Uncle Vernon': 2, 'Fred': 2,
    'George': 2, 'Weasley': 3, 'Draco Malfoy': 3, 'Malfoy': 3
}

def classify_event_type(text):
    text = text.lower()
    if "said" in text or '"' in text:
        return "dialogue"
    elif any(word in text for word in ["died", "killed", "dead"]):
        return "death"
    elif any(word in text for word in ["spell", "magic", "wand", "charm", "curse"]):
        return "magic"
    elif any(word in text for word in ["found", "discovered", "realized"]):
        return "discovery"
    elif any(word in text for word in ["hug", "cry", "smile", "shouted", "angry"]):
        return "emotional"
    elif any(word in text for word in ["ran", "walked", "left", "entered", "arrived"]):
        return "movement"
    else:
        return "other"

def compute_entity_score(entities):
    return sum(entity_weights.get(ent.strip(), 1) for ent in entities)

df['event_type'] = df['event_summary'].apply(classify_event_type)
df['event_type_score'] = df['event_type'].map(event_type_weights).fillna(1)
df['entity_score'] = df['core_entities'].apply(compute_entity_score)

chapter_bounds = df.groupby(['book_num', 'book_title'])['paragraph_num'].agg(['min', 'max']).reset_index()
df = df.merge(chapter_bounds, on=['book_num', 'book_title'], how='left')
df['anchor_bonus'] = df.apply(lambda row: 1 if row['paragraph_num'] in [row['min'], row['max']] else 0, axis=1)

df['importance_score'] = df['event_type_score'] + df['entity_score'] + df['anchor_bonus']

# ========== Step 5: Character Timeline Function (for Streamlit) ==========
def display_character_timeline(character_name: str, upto_book: int, top_k_per_book=5):
    character_name = character_name.strip().lower()

    filtered = df[
        (df['book_num'] < upto_book) &
        (df['character'].str.lower() == character_name)
    ]

    if filtered.empty:
        st.warning(f"No events found for '{character_name}' up to Book {upto_book}")
        return

    st.subheader(f"Timeline for '{character_name.title()}' (Books 1 to {upto_book - 1}):")

    for book in sorted(filtered['book_num'].unique()):
        book_df = filtered[filtered['book_num'] == book]
        top_events = book_df.sort_values(by='importance_score', ascending=False).drop_duplicates(subset='event_summary').head(top_k_per_book)
        top_events = top_events.sort_values(by='paragraph_num')

        st.markdown(f"**Book {book}**")
        for _, row in top_events.iterrows():
            st.markdown(f"  • ({row['importance_score']:.1f} pts) {row['event_summary']}")
            if row['relative_time_cue']:
                st.markdown(f"    ⏱️ Time Cue: {row['relative_time_cue']}")
            if row['semantic_events']:
                st.markdown(f"    🔗 Events: {row['semantic_events']}")

# ========== Step 6: Book Summary Function (for Streamlit) ==========
def display_book_summary(book_number: int, top_k: int = 20):
    book_df = df[df['book_num'] == book_number]
    if book_df.empty:
        st.warning(f"No events found for Book {book_number}")
        return

    st.subheader(f"Summary of Book {book_number} (Top {top_k} Unique Events):")
    top_events = book_df.sort_values(by='importance_score', ascending=False).drop_duplicates(subset='event_summary').head(top_k)
    top_events = top_events.sort_values(by='paragraph_num')
    for _, row in top_events.iterrows():
        st.markdown(f"  • ({row['importance_score']:.1f} pts) {row['event_summary']}")
        if row['relative_time_cue']:
            st.markdown(f"    ⏱️ Time Cue: {row['relative_time_cue']}")
        if row['semantic_events']:
            st.markdown(f"    🔗 Events: {row['semantic_events']}")

# ========== Streamlit App ==========
st.title("Harry Potter Timeline Explorer")

tab1, tab2 = st.tabs(["Character Timeline", "Book Summary"])

with tab1:
    st.header("Character Timeline")
    character_name = st.text_input("Enter Character Name (e.g., Harry Potter)")
    upto_book = st.slider("Timeline Up To Book", 1, df['book_num'].max() if 'book_num' in df.columns else 7, df['book_num'].max() if 'book_num' in df.columns else 7)
    top_k_char = st.slider("Top Events Per Book", 1, 10, 5)
    if st.button("Generate Character Timeline"):
        if character_name:
            display_character_timeline(character_name, upto_book, top_k_char)
        else:
            st.warning("Please enter a character name.")

with tab2:
    st.header("Book Summary")
    book_number = st.slider("Select Book Number", 1, df['book_num'].max() if 'book_num' in df.columns else 7, 1)
    top_k_book = st.slider("Number of Top Events", 5, 30, 20)
    if st.button("Generate Book Summary"):
        display_book_summary(book_number, top_k_book)