import pickle

model, vectorizer = pickle.load(open("models/jailbreak_model.pkl", "rb"))

def is_jailbreak(text):
    vec = vectorizer.transform([text])
    proba = model.predict_proba(vec)[0][1]  # probability of class 1
    return proba > 0.7