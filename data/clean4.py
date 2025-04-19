import pandas as pd
import json

file_path = "removed_character_events.csv"
df = pd.read_csv(file_path)

def infer_location(summary, book, chapter):
    s = summary.lower()
    if "privet drive" in s or "dursley" in s:
        return "Privet Drive"
    elif "hogwarts" in s or "common room" in s or "great hall" in s or "castle" in s:
        return "Hogwarts"
    elif "diagon alley" in s or "ollivanders" in s or "flourish and blotts" in s:
        return "Diagon Alley"
    elif "burrow" in s or "weasley house" in s:
        return "The Burrow"
    elif "ministry of magic" in s or "courtroom" in s or "atrium" in s:
        return "Ministry of Magic"
    elif "gringotts" in s or "bank" in s:
        return "Gringotts"
    elif "forbidden forest" in s or "centaur" in s or "unicorn" in s:
        return "Forbidden Forest"
    elif "hogsmeade" in s or "three broomsticks" in s or "honeydukes" in s:
        return "Hogsmeade"
    elif "leaky cauldron" in s or "pub" in s or "inn" in s:
        return "Leaky Cauldron"
    elif "room of requirement" in s:
        return "Room of Requirement"
    elif "quidditch" in s or "match" in s or "bludger" in s:
        return "Quidditch Pitch"
    elif "chamber of secrets" in s or "basilisk" in s:
        return "Chamber of Secrets"
    elif "azkaban" in s or "dementor" in s:
        return "Azkaban"
    elif "godric's hollow" in s or "graveyard" in s:
        return "Godric's Hollow"
    elif "little hangleton" in s or "riddle house" in s:
        return "Little Hangleton"
    elif "malfoy manor" in s or "lucius" in s or "bellatrix" in s:
        return "Malfoy Manor"
    elif "shell cottage" in s or "bill and fleur" in s:
        return "Shell Cottage"
    elif "grimmauld place" in s or "sirius" in s or "order headquarters" in s:
        return "Number 12 Grimmauld Place"
    elif "maze" in s and "task" in s:
        return "Triwizard Maze"
    else:
        return None

df["location"] = df.apply(lambda row: infer_location(
    row["event_summary"], row["book"], row["chapter_estimate"]
), axis=1)

def format_event_row_with_location(row):
    return {
        "book": row["book"],
        "chapter": int(row["chapter_estimate"]),
        "paragraph": int(row["paragraph_num"]),
        "characters": [c.strip() for c in row["character"].split(",")],
        "event_type": row["event_type"],
        "summary": row["event_summary"],
        "location": row["location"],
        "core_entities": [e.strip() for e in str(row["entities_mentioned"]).split(",")]
    }

structured_data = df.apply(format_event_row_with_location, axis=1).tolist()

output_path = "structured_json_character_events.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(structured_data, f, indent=2, ensure_ascii=False)

print(f"✅ Done! Structured data with locations saved to: {output_path}")
