import spacy

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

def diet_extract(user_input):
    # Define the cuisine names
    diets = ["gluten free", "gluten-free", "gluten", 
                "keto", "ketogenic",
                "vegetarian", "vegan", 
                "pescetarian", "paleo", "primal", "low fodmap", "whole30"]

    # Process the text using the spaCy model
    doc = nlp(user_input)

    # Extract the cuisines from the text
    diet_matches = []
    for token in doc:
        if token.text.lower() in diets:
            if token.text.lower() == "gluten" or token.text.lower() == "gluten-free":
                diet_matches.append("Gluten Free")
            elif token.text.lower() == "keto":
                diet_matches.append("Ketogenic")
            else:
                diet_matches.append(token.text)

    # Print the extracted cuisines
    return diet_matches

# DEMO
# ui = "I am gluten free and keto"
# diet = diet_extract(ui)
# print(diet)