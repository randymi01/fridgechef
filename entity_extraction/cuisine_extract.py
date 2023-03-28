import spacy

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

def cuisine_extract(user_input):
    # Define the cuisine names
    cuisines = ["african", "american", "aritish", "cajun", "caribbean", "chinese", 
                "eastern european", "european", "french", "german", "greek", "indian", 
                "irish", "italian", "japanese", "jewish", "korean", "latin american", 
                "mediterranean", "mexican", "middle eastern", "nordic", "southern", "spanish", "thai", "vietnamese"]

    # Process the text using the spaCy model
    doc = nlp(user_input)

    # Extract the cuisines from the text
    cuisine_matches = []
    for token in doc:
        if token.text.lower() in cuisines:
            cuisine_matches.append(token.text)

    # Print the extracted cuisines
    return cuisine_matches

# DEMO
#ui = "I prefer to eat korean food"
#cuisines = cuisine_extract(ui)
#print(cuisines)
