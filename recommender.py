import time
import requests


def get_recs(user_data, includeNutrition):
    """
    user_data['ingredients'] - list of ingredients that a user has available
    user_data['diet'] - dietary restrictions
    user_data['cuisine'] - preference for type of food
    """
    URL = "https://api.spoonacular.com/recipes/complexSearch"
    
    # Translate list of ingredients to comma-separated list
    ingredients = ""
    for ingredient in user_data['ingredients']:
        ingredients += ingredients + ingredient + ","
    # Remove trailing comma
    ingredients = ingredients[0:len(ingredients) - 1]

    PARAMS = {'apiKey': '10060e3f2d1a4d3d867e05e25e50ecb4',
              'includeIngredients': ingredients,
              'includeInstructions': True,
              'addRecipeInformation': True, 'addRecipeNutrition': includeNutrition,
              'number': 1}
      
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
      
    # extracting data in json format
    data = r.json()

    #'analyzedInstructions', 'nutrition', 'diets', 'cuisines', 
    # 'totalResults' (number of possible matches. NOT the number of results returned). # returned = max(number, totalResults)
    #
    print(data)
          
    return None
