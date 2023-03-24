from transformers import pipeline
import os

# you have to download the model
classifier = pipeline('sentiment-analysis',model="distilbert-base-uncased-finetuned-sst-2-english")


def yn_intent(text: str):
    return classifier(text)[0]['label']

