import spacy

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

def intolerance_extract(user_input):
    # Define the cuisine names
    intolerances = ["dairy", "egg", "gluten", "grain", "peanut", "seafood", "sesame", "shellfish", "soy", "sulfite", "tree nut", "wheat",
                    "nut", "nuts"]

    # Process the text using the spaCy model
    doc = nlp(user_input)

    # Extract the cuisines from the text
    intolerance_matches = []
    for token in doc:
        if token.text.lower() in intolerances:
            if token.text.lower() == "nut" or token.text.lower() == "nuts":
                intolerance_matches.append("peanut")
                intolerance_matches.append("tree nut")
            elif token.text.lower() == "tree":
                pass
            else:
                intolerance_matches.append(token.text)

    # Print the extracted cuisines
    return intolerance_matches

# DEMO
# ui = "I am gluten free and keto"
# diet = diet_extract(ui)
# print(diet)