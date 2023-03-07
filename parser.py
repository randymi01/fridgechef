#Used for pre-processing all the recipes and storing result data into json files
#so we don't have to preprocess everytime a user runs the program





import json
import nltk
nltk.download('averaged_perceptron_tagger')
import difflib as dl
from ingredient_parser import parse_ingredient


#Name to count dictionary
#ingr name as key, ingr count as value
ingredient_counts = {

}

#Used to store finished recipes after ingredients have been parsed
#Key is recipe title, value is ingredients

#parsed_recipes[key: recipe name]{
#
#   ingredients: [
#       {name: "butter", amount: 1, unit: "cup", nrg: 0.0},     NOTE: Calories, fat, protein etc. per ingredient in the recipe
#       ]
#       
#   instructions:[]                      NOTE: Instructions is a list of dictionaries with text as keys
#   nutrition (per 100g): {              NOTE: This is at the recipe level, not ingredient level
#       fat: 3.4,
#       protein: 1.2,
#       ...
#   }
#}


parsed_recipes = {}



ingr_term_blacklist = ["without", "fluid", "hard",
                       "ready-to-serve", "spices",
                       "%", "candies",
                       "double-acting",
                       "regular", "grass-fed",
                       "denny", "varieties",
                       "unenriched", "spartan",
                       "broiler", "mcdonald",
                       "nuts", "crustaceans",
                       "salad dressing", "upc",
                       "cos"]

#Filter to remove exact matches
ingr_match_blacklist = ["nuts", "raw"]

ingr_replace_map = {"leavening" : "baking soda",
                    "salad or cooking" : "olive oil",
                    "skinless" : "chicken breast",
                    "tamari" : "soy sauce",
                    "table" : "salt",
                    "granulated" : "sugar",
                    "margarine" : "margarine",
                    "pancakes" : "pancakes",
                    "snap" : "green beans",
                    "catsup" : "ketchup",
                    "salmon" : "salmon",
                    "cod" : "cod",
                    }


def transform_text(text):
    parts = text.split(',')
    new_text = ""
    # Append descriptors
    for index in range(0, len(parts)):
        descriptor = parts[index]
        descriptor = descriptor.strip()
        add = True

        # Don't add blacklisted ingredients
        for b_ingr in ingr_term_blacklist:
            if (b_ingr in descriptor):
                add = False
                
        for b_ingr in ingr_match_blacklist:
            if (b_ingr == descriptor):
                add = False

        if add:

            for key, value in ingr_replace_map.items():
                if key in descriptor:
                    return value

            if new_text == "":
                new_text = descriptor
            else:
                new_text = descriptor + " " + new_text 

    parsed = parse_ingredient(new_text)
    return parsed["name"]


#Open recipe file to get initial data
with open('recipe_p1.json', 'r') as recipe_file:
    r_file = json.load(recipe_file)

    #Loop through every recipe
    for index in range(len(r_file)):
        recipe = r_file[index]

        recipe_title = recipe["title"]
        #Unparsed ingredients
        r_ingredients = recipe['ingredients']
        
        #Empty dictionary to conform to parsed_recipes dictionary above
        parsed_recipe_data = {
            "ingredients": [],
            "instructions": [], 
            "nutrition": {
                "fat": 0,
                "protein": 0,
                "nrg": 0
            }
        }


        for index, ingr in enumerate(r_ingredients):
            ingr_desc = ingr["text"]
            ingr_name = transform_text(ingr_desc) #Parsed name

            #ingr_dict to be used for recipe storage later  NOTE: add protein and fat as we need it
            ingr_dict = {
                "name": ingr_name,
                "nrg": recipe["nutr_per_ingredient"][index]["nrg"]
            }

            #Add Ingredient data to be used later
            if ingr_name in ingredient_counts:
                ingredient_counts[ingr_name] += 1
            else:
                ingredient_counts[ingr_name] = 1

            parsed_recipe_data["ingredients"].append(ingr_dict)

        parsed_recipe_data["instructions"] = recipe["instructions"]
        #TODO: Add Nutrition data for recipe
        #TODO: Prevent duplicate ingredients in a single recipe (ex: Alternative Cheesecake has butter twice)
        #TODO: Delete recipes that contain an empty ingredient name (ex: Dill butter for...)
        parsed_recipes[recipe_title] = parsed_recipe_data


    # Update ingredient_counts with percentage of recipes that ingredient appears in (divide all counts by total recipes)
    for ingr, count in ingredient_counts.items():
        ingredient_counts[ingr] /= float(len(r_file))

    #Write parsed data to output data for storage and later use
    with open('ingredients.json', 'w') as ingr_file:
        json.dump(ingredient_counts, ingr_file)

    with open('parsed_recipes.json', 'w') as p_file:
        json.dump(parsed_recipes, p_file)


                

            









