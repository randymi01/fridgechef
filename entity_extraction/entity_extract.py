import spacy
from spellchecker import SpellChecker

def food_extract(user_input):
    nlp = spacy.load('entity_extraction/food_ner_model') # load English model

    words = user_input.split()

    spell_check = SpellChecker()

    # Correct typos
    for i, word in enumerate(words):
        idx = len(word) - 1
        punc = ''
        if word[idx] == ',' or word[idx] == '.' or word[idx] == '?' or word[idx] == '!':
            punc = word[idx]
        if not spell_check.unknown([word]):
            words[i] = word + punc
        else:
            words[i] = spell_check.correction(word) + punc
    user_input = ' '.join(words) # spellchecked user input

    processed = nlp(user_input) # process user input
    # Extract ingredients
    ingredients = []
    for entity in processed.ents:
        if entity.label_ == 'FOOD':
            ingredients.append(entity.text.lower())

    ingredients = list(set(ingredients)) # remove duplicate ingredients
    return ingredients

# DEMO
#ui = "I have chicken, kethhup, a lot of butter, salt, and some lemon wedges, and butter. What can I make with these?" # example
#ingredients = food_extract(ui)
#print(ingredients)