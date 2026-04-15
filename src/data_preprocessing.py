import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

# Process jailbreak dataset
jb = pd.read_csv("data/raw/jailbreak_dataset.csv")
jb.drop_duplicates(subset=["text"], inplace=True)
jb.to_csv("data/processed/jailbreak_dataset.csv", index=False)

# Process intent dataset
intent = pd.read_csv("data/raw/intent_dataset.csv")
intent.drop_duplicates(subset=["text"], inplace=True)
intent.to_csv("data/processed/intent_dataset.csv", index=False)

print("Datasets cleaned and saved separately")