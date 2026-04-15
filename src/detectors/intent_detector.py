import pickle

model, vectorizer = pickle.load(open("models/intent_model.pkl", "rb"))

def detect_intent(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]