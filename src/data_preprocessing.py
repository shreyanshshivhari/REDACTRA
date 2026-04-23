import pandas as pd
import os
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Download once (will skip if already installed)
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if pd.isna(text):
        return ""

    text = text.lower()

    # Keep basic punctuation that may carry meaning
    text = re.sub(r"[^a-z0-9\s]", "", text)

    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens).strip()


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

print("Datasets cleaned and preprocessed with lemmatization")