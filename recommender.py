#Used to actually recommend the recipes to the user from the preprocessed data




import json
import nltk
import difflib as dl


#user_ingredients - user inputted ingredients
#recipe - recipe to be given a score
# Assumes user ingredients and recipe ingredients have no repeats.
def score_recipe(user_ingredients, recipe):

    # TODO: Plan is to return the summation of (1 - percent) * calories for all matched ingredients
    matched_ingredients = 0

    for ui in user_ingredients:
        for ri in recipe["ingredients"]:
            if ri["name"] == ui:
                matched_ingredients += 1

    percent = (float(matched_ingredients) / len(recipe["ingredients"]))

    return matched_ingredients + percent



def get_recs(user_ingredients):
    with open("parsed_recipes.json", 'r') as parsed_r_file:
        r_file = json.load(parsed_r_file)
        

        max_score = 0
        max_recipe = ""

        for r in r_file:
            # TODO: Not sure what r_file[r] is. 
            # I think it's best to just pass in the entire recipe entry instead of splitting into variables
            # Makes the function more flexible
            r_score = score_recipe(user_ingredients, r) #, r_file[r])

            if (r_score > max_score):
                max_score = r_score
                max_recipe = r

        print(max_score)
        print(max_recipe)
        print(r_file[max_recipe])
        
        return max_recipe
        



with open("ingredients.json", 'r') as ingredient_file:
    i_file = json.load(ingredient_file)

    ingrs = i_file.keys()

    # TEST USER INPUT (Post entity-extraction)
    input = ["butter", "salmon", "pork", "milk", "bacon", "flour", "ketchup", "spaghetti", "ground beef", "tomato sauce", "onions"]

    parsed_user_ingredients = []
    for user_ingr in input:
        closest_match = dl.get_close_matches(user_ingr, ingrs, 1, 0.6)

        if len(closest_match) == 0:
            print("No match")
        else:
            print(closest_match[0])
            parsed_user_ingredients.append(closest_match[0])


    
    match = get_recs(parsed_user_ingredients)

