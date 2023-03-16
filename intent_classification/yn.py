from transformers import pipeline
import os

if not os.path.exists('models/yn'):
    classifier = pipeline('sentiment-analysis',model="distilbert-base-uncased-finetuned-sst-2-english")
    classifier.save_pretrained(save_directory='models/yn')
else:
    classifier = pipeline('sentiment-analysis',model = "models/yn", tokenizer = "models/yn")

def yn_intent(text: str):
    return classifier(text)[0]['label']

