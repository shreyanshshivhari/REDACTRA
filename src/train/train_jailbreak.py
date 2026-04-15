import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("data/processed/jailbreak_dataset.csv")
X = df["text"]
y = df["label"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

with open("models/jailbreak_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("Jailbreak model trained")