from transformers import pipeline
from jaseci.actions.live_actions import jaseci_action

classifier = pipeline('sentiment-analysis')

@jaseci_action(act_group=["yn_intent"], allow_remote=True)
def yn_intent(text: str):
    return classifier(text)[0]['label']
