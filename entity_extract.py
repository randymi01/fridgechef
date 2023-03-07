import spacy
from spellchecker import SpellChecker

nlp = spacy.load('en_core_web_sm') # load English model

user_input = "blah blah blah (connection to be implemented)"

words = user_input.split()

spell_check = SpellChecker()

# Correct typos
for i, word in enumerate(words):
    if not spell_check.unknown([word]):
        words[i] = word
    else:
        words[i] = spell_check.correction(word)

user_input = ' '.join(words) # spellchecked user input

processed = nlp(user_input) # process user input

# Extract ingredients
ingredients = []
for entity in processed.ents:
    if entity.label_ == 'FOOD':
        ingredients.append(entity.text.lower())

ingredients = list(set(ingredients)) # remove duplicate ingredients

# TODO: send ingredients list to where it needs to be.
