import spacy

# old input sanitation messed up model output
def food_extractor(user_input):
    nlp = spacy.load('food_ner_model_new') # load English model

    return list(map(str,list(nlp(user_input).ents)))