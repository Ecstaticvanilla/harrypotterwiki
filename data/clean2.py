import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("cleaned_character_events.csv", encoding="utf-8", encoding_errors="replace")
df["event_summary"] = (
    df["event_summary"]
    .str.replace("â€œ", '"', regex=False)
    .str.replace("â€", '"', regex=False)
    .str.replace("â€“", "-", regex=False)
)
def classify_event_type(text):
    text = text.lower()

    if any(word in text for word in ["kiss", "hug", "crush", "love", "romantic", "date"]):
        return "romantic"
    elif any(word in text for word in ["cried", "tears", "sad", "shocked", "angry", "afraid", "fear"]):
        return "emotional"
    elif any(word in text for word in ["killed", "duel", "fight", "attacked", "curse"]):
        return "battle"
    elif any(word in text for word in ["found", "discovered", "realized", "learned", "uncovered"]):
        return "discovery"
    elif any(word in text for word in ["went", "left", "arrived", "ran", "came", "entered"]):
        return "movement"
    elif any(word in text for word in ["died", "death", "passed away"]):
        return "death"
    elif any(word in text for word in ["said", "asked", "replied", '"']):
        return "dialogue"
    elif any(word in text for word in ["spell", "wand", "magic", "curse", "charm", "potion"]):
        return "magic"
    else:
        return "other"

event_types = []
entities_list = []

for text in df["event_summary"]:
    doc = nlp(str(text))  

    event_types.append(classify_event_type(text))

    entities = [ent.text for ent in doc.ents if ent.label_ in ("PERSON", "GPE", "ORG", "LOC")]
    entities_list.append(", ".join(entities))

df["event_type"] = event_types
df["entities_mentioned"] = entities_list

df.to_csv("enriched_character_events.csv", index=False)

