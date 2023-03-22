import spacy
from spacy.training import Example
import random
import re

MAX_FOODS_IN_TEMPLATES = 7

food_templates = [
    "I have {}.",
    "I have some {} in my fridge.",
    "Can you suggest a recipe that uses {}?",
    "What can I make with {} and {}?",
    "I need a recipe that includes {}.",
    "I'm trying to use up my {} before they go bad.",
    "What's the best way to cook {}?",
    "I'm looking for a recipe that's gluten-free and uses {}.",
    "What can I do with these leftover {}?",
    "Do you have any recipes that call for {}?",
    "I have a bunch of {} that I need to use soon.",
    "Can you recommend a recipe that uses {} and {}?",
    "What's a good substitute for {} in this recipe?",
    "I'm in the mood for something spicy with {}.",
    "I have some {} that are about to expire.",
    "Can you help me come up with a meal using {}?",
    "I'm looking for a healthy recipe that features {}.",
    "I want to make something vegetarian with {}.",
    "I need a recipe that uses up these extra {}.",
    "What's a good recipe for {} that doesn't take too long?",
    "I'm trying to use up these leftover {} before I go grocery shopping.",
    "I have a lot of {} and I'm not sure what to do with them.",
    "Can you suggest a recipe that's low-carb and uses {}?",
    "I'm looking for a recipe that's easy and only uses {}.",
    "What's a good way to use up these {}?",
    "I need a recipe that's quick and uses {}.",
    "I have {} and {}.",
    "What can I make with these {} and {}?",
    "I have some {} that I don't want to go to waste.",
    "Can you help me find a recipe that features {}?",
    "I'm trying to use up these {} before I move.",
    "I want to make a recipe with {} and {} but I'm not sure what.",
    "What's a good recipe for using up these {}?",
    "I'm looking for a recipe that's dairy-free and uses {}.",
    "I want to make something sweet with {}.",
    "I have some {} that I want to use in a recipe.",
    "Can you suggest a recipe that features {} and {}?",
    "I'm trying to eat healthier and I have a lot of {}.",
    "I need a recipe that's vegetarian and uses {}.",
    "What can I do with these {} that are starting to go bad?",
    "I have a bunch of {} that I need to use up before they expire.",
    "Can you help me come up with a meal that features {}?",
    "I'm looking for a recipe that uses {} and is budget-friendly.",
    "What's a good way to cook {} so that they're crispy?",
    "I'm trying to use up these {} before I go on vacation.",
    "I need a recipe that's low-fat and uses {}.",
    "What can I make with {} that doesn't require too many other ingredients?",
    "I have some {} that I need to use soon, any suggestions?",
    "Can you suggest a recipe that uses up these extra {}?",
    "I'm looking for a recipe that's gluten-free and dairy-free and uses {}.",
    "I want to make a recipe with {} that's a little bit spicy.",
    "What's a good recipe for using up these extra {}?",
    "I have a lot of {} that I need to use before they go bad.",
    "I have some {} and {} in my fridge. What can I make with them?",
    "Can you suggest a recipe that uses {} and {} together?",
    "I want to make a dish with {} and {}. What do you recommend?",
    "I have {}, {}, and {}.",
    "I have {} and {} that I need to use up. Any ideas?",
    "What's a good recipe that uses {} and {} as the main ingredients?",
    "I'm looking for a recipe that features {} and {} in equal amounts.",
    "I want to make a recipe that combines {} and {}. Do you have any suggestions?",
    "I have {} and {} that I want to use in a recipe. What can I make?",
    "What's a good way to use up these {} and {} that I have leftover?",
    "Can you suggest a recipe that uses both {} and {} in a creative way?",
    "I want to make a recipe that includes {} and {}. Any ideas?",
    "I'm looking for a recipe that uses up my excess {} and {}.",
    "What can I make with these {} and {} that will feed a crowd?",
    "I have a lot of {} and {}. What's a good recipe to use them up?",
    "I have {}, {}, and {} in my pantry. What can I make with them?",
    "Can you suggest a recipe that uses {} along with {} and {}?",
    "I have {}, {}, {}, and {}.",
    "I want to make a dish that features {} and {}, but also includes {}. Any ideas?",
    "I have {} and {} that need to be used up, along with {}. What can I make?",
    "What's a good recipe that uses {} as well as {} and {}?",
    "I'm looking for a recipe that combines {}, {}, and {} in a unique way.",
    "I want to make a recipe that uses both {} and {}, as well as {}. Do you have any suggestions?",
    "I have a lot of {} and {}, but also some {}. What can I make with them?",
    "What's a good way to use up my excess {} and {}, along with some {}?",
    "Can you suggest a recipe that incorporates {} and {}, but also features {} and {}?",
    "I want to make a recipe that includes {}, {}, and {}. Any ideas?",
    "I have some {} and {} that need to be used up, along with {}. What can I make?",
    "What can I make with {} as well as {} and {}?",
    "I'm looking for a recipe that features {} and {}, along with some {} and {}.",
    "I have {}, {}, {}, {} and {}.",
    "Can you suggest a recipe that uses up my excess {}, along with {} and {}?",
    "I have a surplus of {}, along with {} and {}. What's a good recipe that uses them up?",
    "What's a good way to incorporate {} and {} into a recipe that already includes {} and {}?",
    "I want to make a recipe that uses {}, {}, and {}, but also features some {} and {}.",
    "Can you suggest a recipe that uses up my extra {} and {}, along with some {} and {}?",
    "I have a lot of {}, {}, and {}. What can I make with them?",
    "What's a good recipe that combines {} and {}, along with some {} and {}?",
    "I want to make a dish that includes {}, {}, and {} in equal amounts.",
    "Can you suggest a recipe that features {}, {}, and {}, but also uses some {} and {}?",
    "I have some {} and {}, but also some {}. What can I make with them?",
    "What's a good way to use up my surplus of {}, along with some {} and {}?",
    "I have {}, {}, some {}, {}, {} and a little {}.",
    "I want to make a recipe that incorporates {}, {}, and {}, but also features some {} and {}.",
    "Can you suggest a recipe that uses up my extra {} and {}, but also includes some {} and {}?",
    "I have {}, {}, and {} that I need to use up. What can I make?",
    "What's a good recipe that uses {} and {}, along with some {} and {}?",
    "I'm looking for a recipe that combines {}, {}, and {} in a tasty way.",
    "I want to make a dish that includes {}, {}, and {} as the main ingredients.",
    "Can you suggest a recipe that uses {}, {}, and {} in equal amounts?",
    "I have {}, {}, a few {}, {}, a lot of {}, {} and {}.",
    "I have a lot of {}, {}, and {}. What's a good recipe that incorporates them all?",
    "What's a good way to use up my excess of {}, {}, and {}, along with some {} and {}?",
    "I want to make a recipe that features {}, {}, and {}, but also includes some {} and {}.",
    "Can you suggest a recipe that uses up my extra {} and {}, but also features some {} and {}?",
    "I have a surplus of {}, {}, and {}, along with some {} and {}. What can I make with them?"
]

# Remove ending punctuation from 75% of food templates
count = 1
for temp in food_templates:
    if count != 4:
        temp = temp[:-1]
        count = count + 1
    else:
        count = 1

with open('generic-food.csv', 'r') as file:
    foods = file.read().split('\n')

# Remove capitalization of foods
for idx in range(len(foods)):
    foods[idx] = foods[idx][0].lower() + foods[idx][1:]

train_data = []
for i in range(5):
    food_count = len(foods) - 1
    random.shuffle(foods)
    while food_count >= MAX_FOODS_IN_TEMPLATES:
        entities = []

        # Random UI template
        template = food_templates[random.randint(0, len(food_templates) - 1)]

        # Find {} to be replaced
        matches = re.findall("{}", template)

        # Replace each {} with food
        last_idx = 0
        for match in matches:
            food = foods[food_count]
            food_count -= 1

            # Replace and find start and end indices of food entities
            template = template.replace(match, food, 1)
            match_span = re.search(food, template[last_idx:]).span()

            # Append to list of entities in template
            entities.append((match_span[0] + last_idx, match_span[1] + last_idx, "FOOD"))
            last_idx += match_span[1]

        # Append template and entities to training data
        train_data.append((template, {"entities": entities}))

nlp = spacy.blank("en")

# Create food label
ner = nlp.add_pipe("ner")
ner.add_label("FOOD")

# Train the model
optimizer = nlp.initialize()
n_iter = 10
for i in range(n_iter):
    random.shuffle(train_data)
    losses = {}
    for raw_text, entity_offsets in train_data:
        doc = nlp.make_doc(raw_text)
        example = Example.from_dict(doc, entity_offsets)
        nlp.update([example], sgd=optimizer, losses=losses, drop=0.25)
    print(f"Iteration {i}: Loss = {losses['ner']}")

# Save the model
nlp.to_disk("food_ner_model")