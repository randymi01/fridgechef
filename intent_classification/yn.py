from transformers import pipeline

classifier = pipeline('sentiment-analysis')

def yn_intent(text: str):
    print(classifier(text)[0]['label'])
    return classifier(text)[0]['label']

