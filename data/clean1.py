import pandas as pd
import re

df = pd.read_csv("character_events.csv")
df = df.drop_duplicates()
df = df.dropna(subset=["event_summary", "character"])
df["character"] = df["character"].str.strip().str.title()
df["book"] = df["book"].str.replace(r"^\d+\s*", "", regex=True)
df = df[df["event_summary"].str.len() > 10]
df["event_type"] = "unknown" 
df["chapter_estimate"] = (df["paragraph_num"] // 100) + 1
df = df.reset_index(drop=True)
print(df.head())
df.to_csv("cleaned_character_events.csv", index=False)
