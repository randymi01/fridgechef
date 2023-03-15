from transformers import pipeline

classifier = pipeline('sentiment-analysis')

def yn_intent(text: str):
    return classifier(text)[0]['label']

