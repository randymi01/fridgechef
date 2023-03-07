#Used to actually recommend the recipes to the user from the preprocessed data




import json
import nltk
import difflib as dl


#user_ingredients - user inputted ingredients
#recipe - recipe to be given a score
# Assumes user ingredients and recipe ingredients have no repeats.
def score_recipe(user_ingredients, name, recipe):

    # TODO: REMOVE INGR IF STATEMENT
    if len(recipe["ingredients"]) < 5:
        return 0
    matched_ingredients = []
    total_energy = 0
    missing_ingredients = []

    for ri in recipe["ingredients"]:
        ingr_matched = False
        for ui in user_ingredients:
            total_energy += ri["nrg"]
            if ri["name"] == ui["name"]: # Ingredient is a match
                matched_ingredients.append({
                    "name": ri["name"],
                    "nrg": ri["nrg"],
                    "recipe_commonality_percent": ui["count"]
                    })

                ingr_matched = True
                break
        
        if not ingr_matched: # Ingredient is missing
            missing_ingredients.append(ri)

    # Count number of missing 'essential' ingredients
    missing_important_ingr_count = 0
    for missing_ingr in missing_ingredients:
        if missing_ingr["nrg"] > 0 and missing_ingr["nrg"] / total_energy > 0.2: # If ingredient takes up > 20% of energy of meal, it is important
            missing_important_ingr_count += 1


    # Calculate matched_ingredient_score
    matched_ingredient_score = 0
    for matched_ingr in matched_ingredients:
        matched_ingredient_score += (1-matched_ingr["recipe_commonality_percent"]) * (matched_ingr["nrg"] / total_energy)

    score = matched_ingredient_score + -0.1 * missing_important_ingr_count

    return score



def get_recs(user_ingredients):
    with open("parsed_recipes.json", 'r') as parsed_r_file:
        r_file = json.load(parsed_r_file)
        

        max_score = 0
        max_recipe = ""
        for r in r_file:
            if r == "Very Easy Alternative Cheesecake Base" or r == "Clarified butter" or r == "Clarified Butter":
                continue
            r_score = score_recipe(user_ingredients, r, r_file[r]) #, r_file[r])
            if (r_score > max_score):
                max_score = r_score
                max_recipe = r

        print(max_score)
        print(max_recipe)
        print(r_file[max_recipe]["ingredients"])
        print(user_ingredients)
        
        return max_recipe
        



with open("ingredients.json", 'r') as ingredient_file:
    i_file = json.load(ingredient_file)
    
    ingrs = i_file.keys()

    # TEST USER INPUT (Post entity-extraction)
    input = ["salmon", "pork", "milk", "bacon", "flour", "ketchup", "spaghetti", "ground beef", "tomato sauce", "onions"]

    parsed_user_ingredients = []
    for user_ingr in input:
        closest_match = dl.get_close_matches(user_ingr, ingrs, 1, 0.6)

        if len(closest_match) == 0:
            print("No match")
        else:
            print(closest_match[0])
            parsed_user_ingredients.append({
                "name": closest_match[0],
                "count": i_file[closest_match[0]]
                })
    
    match = get_recs(parsed_user_ingredients)

