import requests

# Improvement Ideas:
# 1. Fetch top X missing and top X used and bottom X missing and bottom X used (X = count)
# 1b. Filter any possible matching recipes
# 2. Sort by custom scoring algorithm (Can use one from before)
# 3. Return top 'count' recipes

# Ignore 'offset' for now. More logic can be implemented later if necessary

def list_to_str(my_list):
    list_str = ""
    for item in my_list:
        item = item.replace(" ", "_")
        list_str += item + ","
    # Remove trailing comma
    list_str = list_str[0:len(list_str) - 1]
    return list_str


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

    # Score settings
    missing_essential_mult = -3 # Missing penalized more than used
    missing_noness_mult = -0.5
    used_essential_mult = 1
    used_noness_mult = 0.5

    score = (missing_essential_mult*num_missing_essential
              + missing_noness_mult*num_missed_noness
              + used_essential_mult*num_used_essential
              + used_noness_mult*num_used_noness)

    return score

def make_request(ingredients, count, diet, cuisine, mode):
    """
    mode (int) - 0 = asc missing, 1 = desc missing, 2 = asc used, 3 = desc used
    See get_recs for descriptions of all other inputs
    """
    
    # TODO: Play with how many recipes and of what type should be fetched. And play with scoring function (it seems biased against one of the sort strategies)
    if mode == 0:
        sort = "min-missing-ingredients"
        direction = "asc"
    elif mode == 1:
        sort = "random" # NOTE: Desc sort direction seems to be broken. Using random instead to get some extra possibilities
        direction = "asc"
    elif mode == 2:
        sort = "max-used-ingredients"
        direction = "asc"
    elif mode == 3:
        sort = "random" # NOTE: Desc sort direction seems to be broken. Using random instead to get some extra possibilities
        direction = "asc"
    else:
        print(f"Error: Invalid mode. Specified {mode}. Mode must be an integer in range 0-3")
        return None
    
    URL = "https://api.spoonacular.com/recipes/complexSearch"
    
    # Translate list of ingredients to comma-separated list
    ingredients_str = list_to_str(ingredients)

    # Initialize parameters. Required items stated here
    PARAMS = {'apiKey': '10060e3f2d1a4d3d867e05e25e50ecb4',
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
      
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
      
    # extracting data in json format
    data = r.json()

    return data

def filter_and_combine(*queries):
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
        recipe['score'] = score

    # Sort them
    sorted_data = sorted(data, key=lambda d: d['score'])

    # Return top 'count'
    if len(sorted_data) >= count:
        return sorted_data[0:count]
    else:
        return sorted_data # Return all of them


def get_recs(ingredients, count=1, diet=None, cuisine=None):
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
    # Check count bounds
    if count > 40:
        count = 40
    elif count < 0:
        return []
    
    data0 = make_request(ingredients, count, diet, cuisine, 0)
    data1 = make_request(ingredients, count, diet, cuisine, 1)
    data2 = make_request(ingredients, count, diet, cuisine, 2)
    data3 = make_request(ingredients, count, diet, cuisine, 3)

    # Filter duplicate recipes
    data = filter_and_combine(data0, data1, data2, data3) # Final set of recipes to decide from

    #print(f"Unscored data: {data} \n \n ")

    # Score recipes to find top 'count' highest
    data = get_best(data, count)

    print(f"Best data: {data} \n \n ")

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
            'instructions': instructions
        }

        results.append(recommendation)


    recommendations = {
        'number': len(data),
        'results': results
    }

    return recommendations