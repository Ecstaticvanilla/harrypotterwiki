import pandas as pd
import re

df = pd.read_csv("enriched_character_events.csv", encoding="utf-8")

import pandas as pd
import numpy as np

def clean_entities(entities_str):
    if isinstance(entities_str, str): 
        cleaned = entities_str.replace("â€™", "'")
        return cleaned
    else:
        return entities_str  

df["entities_mentioned"] = df["entities_mentioned"].apply(clean_entities)


df["entities_mentioned"] = df["entities_mentioned"].apply(clean_entities)

df["event_summary"] = df["event_summary"].apply(lambda x: x.replace("â€™", "'"))

df.to_csv("removed_character_events.csv", index=False)

print(df.head())
