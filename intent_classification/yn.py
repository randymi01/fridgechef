from transformers import pipeline
from jaseci.actions.live_actions import jaseci_action

classifier = pipeline('sentiment-analysis')

#TODO save model so don't have to download everytime at runtime

@jaseci_action(act_group=["intent"], allow_remote=True)
def yn(text: str):
    return 'yes' if classifier(text)[0]['label'] == "POSITIVE" else 'no'