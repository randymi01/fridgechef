import spacy
from spellchecker import SpellChecker

nlp = spacy.load('food_ner_model') # load English model

user_input = "I have chicken, ketchup, a lot of butter, salt, and some lemon wedges. What can I make with these?" # DEMO - it works!

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

# TODO: send ingredients list to where it needs to be.

print(ingredients)