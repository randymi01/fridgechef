import json
import nltk
import difflib as dl
nltk.download('averaged_perceptron_tagger')
from ingredient_parser import parse_ingredient


# https://towardsdatascience.com/embedding-contexts-into-recipe-ingredients-709a95841914

# Idea - user can specify ingredients they do NOT have
ingr_term_blacklist = ["without", "fluid", "hard",
                       "ready-to-serve", "spices",
                       "%", "candies",
                       "double-acting", "raw",
                       "regular", "grass-fed",
                       "denny", "varieties",
                       "unenriched", "spartan"]
ingr_replace_map = {"leavening" : "baking soda",
                    "oil, olive" : "olive oil"}
                       # leavening agents, yeast, baker's, active dry

# our_recipes['id'] = { # id taken from dataset
#     original_ingredients: set(), # Original ingredients from dataset
#     ingredients: set(), # Parsed ingredients
#     instructions: [], # Ordered list of strings for instructions
# }
our_recipes = {}


# Pre-processing master set of ingredients

#parsed_ingredients["name"] = {
#    "count": 0
#}
parsed_ingredients = {}
default_ingr = {
    "count": 0
}

def score(user_ingredients, recipe):
    """
    user_ingredients (set) - ingredients (post entity-extraction) that user has available
    recipe - dictionary of recipe. Used to make scoring function more flexible to additional recipe parameters
    recipe["ingredients"] (set) - ingredients (post entity-extraction) of the recipe

    Returns float value between 0-1. Higher score indicates better match.

    """
    recipe_ingredients = recipe["ingredients"]

    # Find ingredients that both user and recipe have
    intersect = user_ingredients.intersection(recipe_ingredients)

    # TODO: Modify to check commonality of ingredients

    # Percentage of ingredients user has in the recipe
    return float(len(intersect)) / len(recipe_ingredients)
    

def transform_text(text):
    parts = text.split(',')
    new_text = ""
    # Append descriptors
    for index in range(0, min(len(parts), 3)):
        ingr = parts[index]
        add = True
        # Don't add blacklisted ingredients
        for b_ingr in ingr_term_blacklist:
            if b_ingr in ingr:
                add = False
                
        if add:
            # Replace ingredient name if... weird
            for key, value in ingr_replace_map.items():
                if key in ingr:
                    return value
                
            new_text = ingr + " " + new_text  

    return new_text


with open('100recipes.json', 'r') as recipe_file:
    r_file = json.load(recipe_file)

    print(len(r_file))
    for index in range(0, 100):
        recipe = r_file[index]

        #Grab relevant data from the recipes
        ingredients = recipe['ingredients']
        adjusted_ingredients = set()
        instructions = recipe['instructions']
        id = recipe['id']
        

        for ingr in ingredients:
            #print(ingr["text"])
            # print(transform_text(ingr["text"]))
            parsed_i = parse_ingredient(transform_text(ingr["text"]))
            #print(parsed_i["name"])

            adjusted_ingredients.add(parsed_i["name"])
            parsed_ingredients.get(parsed_i["name"], default_ingr)["count"] += 1



            #parsed_ingredients.add(parsed_i["name"])
            
            #print("\n ")

        
        ingredient_set = set()

        for ingr in ingredients:
            ingredient_set.add(ingr["text"])


        #Add relevant data to database, maybe github for storage later?
        our_recipes[id] = {
            "original_ingredients": ingredient_set,
            "ingredients": adjusted_ingredients, 
            "instructions": instructions
            }
        

    input = {"milk", "tortillas", "bell pepper", "chicken", "salsa", "sour cream", "cheese", "pasta", "rice", "salt", "butter", "onions"}
    correct_recipe_id = "0005fc89f7" # Used for testing purposes
    matched_input = set()

    for user_ingredient in input:
        #Find closest ingredient to one user provided
        closest_i = dl.get_close_matches(user_ingredient, parsed_ingredients, 1, 0.5) # TODO: Modify this to use key set

        #If user inputs garbage skip
        if len(closest_i) == 0 :
            print("No match")
            continue

        print(f"User input: {user_ingredient}")
        print(f"Closest Match: {closest_i}")
        matched_input.add(closest_i[0])


    # Number of best matched recipes to find
    recipe_count = 2

    # TEMP - just find only 1 recipe
    best_recipe = None
    best_recipe_score = -1
    for recipe_id, our_recipe in our_recipes.items():
        recipe_score = score(matched_input, our_recipe)

        if recipe_score > best_recipe_score:
            best_recipe = our_recipe
            best_recipe_score = recipe_score

    best_ingr = best_recipe["ingredients"]
    print(f"Best recipe ({best_recipe_score}): \n{best_ingr}")



        
        
        
        
        
# Ideas - take first chunk before comma, unless it's 'oil' or 'spices'
# olive oil
# ingredient type - oil
# ingredient metadata - olive, salad or cooking

        #print(r_file[recipe]['ingredients'])
# {'text': 'spartan, real semi-sweet chocolate baking chips, upc: 011213162966'}

# {'text': 'leavening agents, baking powder, double-acting, sodium aluminum sulfate'}

# {'text': 'oil, corn, peanut, and olive'} -- substitutes

# {'text': 'egg substitute, powder'}
