import requests
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import secret
import threading

# Revision history
# 4/1/23 (Kyle) - Added more queries! For every user input ingredient, we query spoonacular for similar ingredients to capture more possible
# recipes and ingredients (ie: chicken becomes chicken breast, chicken thigh, chicken broth, chicken feet, chicken nugget...)
# 4/1/23 (Kyle) - Added much lower limits for the get_recs() function. Only returns 1 recipe recommendation and only 7 user ingredients allowed.
# This is only for testing purposes... with so many queries, we hit our daily quota pretty quickly
# 4/1/23 (Kyle) - modified scoring function. Changed parameters and also added to the score if there are more ingredients in the recipe (total / 2)
# 4/2/23 (Kyle) - parallelize calls to spoonacular api
# 4/2/23 (Jacob) - Small change to boost recipes with all essential ingredients
# 4/3/23 (Kyle) - Fixed ranking in incorrect order.
# 4/8/23 (Kyle) - Remove quota limits
token = secret.SPOON_AUTH

def list_to_str(my_list):
    list_str = ""
    for item in my_list:
        list_str += item + ","
    # Remove trailing comma
    list_str = list_str[0:len(list_str) - 1]
    return list_str

def make_ingr_request(ingredient, results):
    URL = "https://api.spoonacular.com/food/ingredients/search"

    # Initialize parameters. Required items stated here
    PARAMS = {'apiKey': token,
              'query': ingredient,
              'number': 20} # Adding to this number does not harm our query limit
      
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
      
    # extracting data in json format
    data = r.json()

    print(f"Data ({ingredient}) : {data['results']} \n \n ")
    results.append(data)

def improve_ingredients(ingredients):
    new_ingrs = set()
    threads = []
    datas = []
    for user_ingr in ingredients:
        user_ingr = user_ingr.lower()
        # Add original queried ingredient
        new_ingrs.add(user_ingr)
        # # Skip query for ingredients that have more than one word already - helps reduce unnecessary queries/ingredients
        # if len(user_ingr.split()) > 1:
        #     continue
        # Make query in new thread
        t = threading.Thread(target=make_ingr_request, args=(user_ingr, datas))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    for data in datas:
        # Add variations of ingredient
        for result in data['results']:
            name = result['name']
            if len(name.split()) <= 2: # Only add ingredients with up to 2 words (filters out things that are too specific)
                new_ingrs.add(name.lower())
    return new_ingrs


def get_calories(recipe_or_ingr):
    """
    Find calories in either recipe OR ingredient (works for both)
    """
    for nutrient in recipe_or_ingr['nutrients']:
        if nutrient['name'] == 'Calories':
            if nutrient['unit'] == 'kcal':
                return nutrient['amount']
            else:
                return 0
    # Calories not found
    return 0

def get_essentials_info(recipe):

    # Create set of used ids
    used_ids = set()
    for ingr in recipe['usedIngredients']:
        used_ids.add(ingr['id'])

    # Create set of missing ids
    missed_ids = set()
    for ingr in recipe['missedIngredients']:
        missed_ids.add(ingr['id'])

    total_energy = get_calories(recipe['nutrition'])
    num_used_essential = 0
    num_missing_essential = 0
    for ingredient in recipe['nutrition']['ingredients']:
        calories = get_calories(ingredient)
        # ingredient is 'essential' if it has calories greater than 10% of total meal
        if calories / total_energy > 0.10:
            id = ingredient['id']
            if id in used_ids:
                num_used_essential += 1
            elif id in missed_ids:
                num_missing_essential += 1

    return num_used_essential, num_missing_essential


def score_recipe(recipe):

    num_used_essential, num_missing_essential = get_essentials_info(recipe)
    num_used_noness = recipe['usedIngredientCount'] - num_used_essential
    num_missed_noness = recipe['missedIngredientCount'] - num_missing_essential
    # Used to help get recipes with more ingredients in results
    total = recipe['usedIngredientCount'] + recipe['missedIngredientCount']

    # Score settings
    missing_essential_mult = -3 # Missing penalized more than used
    missing_noness_mult = 0
    used_essential_mult = 1
    used_noness_mult = 0.5

    score = (total / 2) + (missing_essential_mult*num_missing_essential
              + missing_noness_mult*num_missed_noness
              + used_essential_mult*num_used_essential
              + used_noness_mult*num_used_noness)

    if num_missing_essential == 0:
        score = score + 1

    return score

def make_request(ingredients, count, allergies, diet, intolerances, cuisine, mode, results):
    """
    mode (int) - 0 = asc missing, 1 = asc used
    See get_recs for descriptions of all other inputs
    """
    
    if mode == 0:
        sort = "min-missing-ingredients"
        direction = "asc"
    elif mode == 1:
        sort = "max-used-ingredients"
        direction = "asc"
    else:
        print(f"Error: Invalid mode. Specified {mode}. Mode must be an integer in range 0-1")
    
    URL = "https://api.spoonacular.com/recipes/complexSearch"
    
    # Translate list of ingredients to comma-separated list
    ingredients_str = list_to_str(ingredients)

    # Initialize parameters. Required items stated here
    PARAMS = {'apiKey': token,
              'includeIngredients': ingredients_str,
              'fillIngredients': True,
              'instructionsRequired': True,
              'addRecipeInformation': True, 
              'addRecipeNutrition': True,
              'type': 'main_course',
              'sort': sort,
              'sortDirection': direction,
              'number': count}

    # Add optional parameters
    if diet is not None:
        PARAMS['diet'] = list_to_str(diet)

    if cuisine is not None:
        PARAMS['cuisine'] = list_to_str(cuisine)
    
    if allergies is not None:
        PARAMS['excludeIngredients'] = list_to_str(allergies)
    
    if intolerances is not None:
        PARAMS['intolerances'] = list_to_str(intolerances)
      
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
      
    # extracting data in json format
    data = r.json()

    # Add sort and sort direction data - TODO: REMOVE, DEBUG ONLY
    print(f"Found {len(data['results'])} results")
    for recipe in data['results']:
        recipe['mySort'] = sort
        recipe['myDirection'] = direction

    results.append(data)

def filter_and_combine(queries):
    ids = set()
    filtered_recipes = []
    for query in queries:
        for recipe in query['results']:
            id = recipe['id']
            if id in ids:
                print(f"FILTERED OUT: {id}")
                continue
            else:
                filtered_recipes.append(recipe)
                ids.add(id)
    return filtered_recipes

def get_best(data, count):
    # Score all recipes
    for recipe in data:
        score = score_recipe(recipe)
        print(f"Score ({recipe['id']}): {score} ")
        recipe['score'] = score

    # Sort them by score (descending)
    sorted_data = sorted(data, key=lambda d: -1*d['score'])

    # Return top 'count'
    if len(sorted_data) >= count:
        print(f"Ruled out: {extract_recs(sorted_data[0:len(sorted_data)])} \n \n ")
        return sorted_data[0:count]
    else:
        return sorted_data # Return all of them
    
def extract_recs(data):
    # Loop through results
    results = []
    for result in data:

        # Add ingredients list
        ingredients = []
        for ingredient in result['extendedIngredients']:
            ingredients.append((ingredient['nameClean'], float(ingredient['amount']), ingredient['unit']))

        # Add instructions - 
        instructions = []
        if len(result['analyzedInstructions']) > 0: # added this to prevent error when recipe has no instructions, which I was getting earlier but I have no longer??
            for instruction in result['analyzedInstructions'][0]['steps']:
                instructions.append(instruction['step'])


        recommendation = {
            'title': result['title'],
            'readyInMinutes': result['readyInMinutes'],
            'servings': result['servings'],
            'usedIngredientCount': result['usedIngredientCount'],
            'missedIngredientCount': result['missedIngredientCount'],
            'ingredients': ingredients,
            'instructions': instructions,
            'score': result['score'],
            'id': result['id'],
        }

        results.append(recommendation)


    recommendations = {
        'number': len(data),
        'results': results
    }
    return recommendations


def get_recs(ingredients, count=1, allergies=None, diet=None, intolerances=None, cuisine=None):
    """
    Parameters:

    ingredients - list of ingredients that a user has available
    count (optional) - number of recommendations (0-40) to try to retrieve (NOTE: This does not guarantee this many recommendations are found). Default is 1
    diet (optional) - dietary restrictions. Must be a LIST of strings from here: https://spoonacular.com/food-api/docs#Diets. Recommendations will include only those that satisfy ALL diets in the list
    cuisine (optional) - limit to only recommendations of this cuisine. Must be a string from here: https://spoonacular.com/food-api/docs#Cuisines

    Returns:

    data (dict):
        data['number'] (int) - number of recommendations returned (not necessarily equal to the count parameter)
        data['results'] (list) - list of recommendations
            data['results'][i] (dict) - dictionary storing recommendation information
                data['results'][i]['title'] (str) - title for recipe
                data['results'][i]['servings'] (float) - number of servings the recipe makes
                data['results'][i]['readyInMinutes'] - how long to make
                data['results'][i]['ingredients'] - list of 3 tuples (name (str), amount (float), unit (str))
                data['results'][i]['instructions'] - ordered string list of instructions
    """

    ### DAILY QUOTA LIMIT CHECKS - used to ensure daily quota isn't reached too quickly

    # Check count bounds
    # if count > 1:
    #     count = 1
    # elif count < 0:
    #     return []
    
    # # Trim list, again for daily quota. Can be removed later on
    # if len(ingredients) > 7:
    #     ingredients = ingredients[0:7] # Trim list

    ### END DAILY QUOTA LIMIT CHECKS
    
    # Create new list of ingredients based on user input. Finds similar ingredients and appends to original ingredients list
    # ingredients = improve_ingredients(ingredients) # TODO: Re-add for demo?

    # print(f"New ingr: {ingredients}")
    
    threads = []
    results = []
    
    t0 = threading.Thread(target=make_request, args=(ingredients, count, allergies, diet, intolerances, cuisine, 0, results))
    threads.append(t0)
    t0.start()

    t1 = threading.Thread(target=make_request, args=(ingredients, count, allergies, diet, intolerances, cuisine, 1, results))
    threads.append(t1)
    t1.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Filter duplicate recipes
    data = filter_and_combine(results) # Final set of recipes to decide from

    #print(f"Unscored data: {data} \n \n ")

    # Score recipes to find top 'count' highest
    data = get_best(data, count)

    print("Best recipe data:")
    for recipe in data:
        print(f"  Id: {recipe['id']} sort: {recipe['mySort']} dir: {recipe['myDirection']}")


    recommendations = extract_recs(data)
    return recommendations