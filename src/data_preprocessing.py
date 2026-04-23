import pandas as pd
import os
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = text.strip()
    return text

os.makedirs("data/processed", exist_ok=True)

# Process jailbreak dataset
jb = pd.read_csv("data/raw/jailbreak_dataset.csv")
jb.drop_duplicates(subset=["text"], inplace=True)
jb["text"] = jb["text"].apply(clean_text)
jb.to_csv("data/processed/jailbreak_dataset.csv", index=False)

# Process intent dataset
intent = pd.read_csv("data/raw/intent_dataset.csv")
intent.drop_duplicates(subset=["text"], inplace=True)
intent["text"] = intent["text"].apply(clean_text)
intent.to_csv("data/processed/intent_dataset.csv", index=False)

print("Datasets cleaned and preprocessed")