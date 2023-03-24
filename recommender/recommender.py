import requests

def list_to_str(my_list):
    list_str = ""
    for item in my_list:
        list_str += list_str + item + ","
    # Remove trailing comma
    list_str = list_str[0:len(list_str) - 1]

def get_recs(ingredients, count=1, diet=None, cuisine=None, includeNutrition=False):
    """
    Parameters:

    ingredients - list of ingredients that a user has available
    count (optional) - number of recommendations to try to retrieve (NOTE: This does not guarantee this many recommendations are found). Default is 1
    diet (optional) - dietary restrictions. Must be a LIST of strings from here: https://spoonacular.com/food-api/docs#Diets. Recommendations will include only those that satisfy ALL diets in the list
    cuisine (optional) - limit to only recommendations of this cuisine. Must be a string from here: https://spoonacular.com/food-api/docs#Cuisines
    includeNutrition (optional) - whether to return extra nutritional information. Default is False

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
    URL = "https://api.spoonacular.com/recipes/complexSearch"
    
    # Translate list of ingredients to comma-separated list
    ingredients_str = list_to_str(ingredients)

    # Initialize parameters. Required items stated here
    PARAMS = {'apiKey': '10060e3f2d1a4d3d867e05e25e50ecb4',
              'includeIngredients': ingredients_str,
              'fillIngredients': True,
              'includeInstructions': True,
              'addRecipeInformation': True, 
              'addRecipeNutrition': includeNutrition,
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

    # Loop through results
    results = []
    for result in data['results']:

        # Add ingredients list - Liam
        ingredients = []
        # NOTE: Tuple should be (name (str), amount (float), unit (str))

        # Add instructions - 
        instructions = []
        for instruction in result['analyzedInstructions']['steps']:
            instructions.append(instruction['step'])


        recommendation = {
            'title': result['title'],
            'readyInMinutes': result['readyInMinutes'],
            'servings': result['servings'],
            'ingredients': ingredients,
            'instructions': instructions
        }

        results.append(recommendation)


    recommendations = {
        'number': len(data['results']),
        'results': results
    }

    return recommendations

    # TODO: Remove data that we do not need
            # data['results'][0]['readyInMinutes'] - done
            # data['results'][0]['servings'] - done
            # data['results'] - recommendations
            # data['number'] - recommendations found - done
            # data['results'][0]['ingredients'] - LIST of 3 TUPLES
            # - 'ingredients' (name, amount, unit)
    # return data