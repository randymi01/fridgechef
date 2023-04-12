import time
import requests

#This did not make the final project, but the following is a machine leaning algorithm that can take in a
# list of rankings for spoonacular recipes and uses ML to find parameters that help sort new recipes.

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
              'fillIngredients': True,
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


# In[2]:


# data['results'] - recommendations
# data['number'] - recommendations found
# data['results'][0]
# data['results'][0]['ingredients'] - LIST of TUPLES
# - 'ingredients' (name, amount, unit), 'instructions' (list of steps in order), 'title'
# return data



URL = "https://api.spoonacular.com/recipes/complexSearch"
PARAMS = {'apiKey': '10060e3f2d1a4d3d867e05e25e50ecb4',
              'includeIngredients': ['spaghetti', 'apples', 'tomatoes', 'tofu', 'bread', 'mushrooms', 'tomato sauce'],
              'fillIngredients': True,
              'includeInstructions': True,
              'addRecipeInformation': True, 'addRecipeNutrition': [],
              'number': 2}
r = requests.get(url = URL, params = PARAMS)
js = r.json()


# for h in range(len(js['results'])):
#     js['results'].append({})
#     js['results'][-1]['ingredients'] = []
#     for i in range(len(js['results'][h]['analyzedInstructions'][0]['steps'])):
#         for j in range(len(js['results'][h]['analyzedInstructions'][0]['steps'][i]['ingredients'])):
#             js['results'][-1]['ingredients'].append(js['results'][h]['analyzedInstructions'][0]['steps'][i]['ingredients'][j]['name'])
            
# print(js['results'])

print(js['results'][0]['extendedIngredients'][0]['measures']['us'])


# In[3]:


data = {}
data['number'] = len(js['results'])
data['results'] = []
for i in range(len(js['results'])-1):
    data['results'].append({})
    data['results'][-1]['title'] = js['results'][i]['title']
    data['results'][-1]['instructions']= 0
    data['results'][-1]['ingredients'] = []
    for j in range(len(js['results'][-1]['extendedIngredients'])):
        lst = js['results'][-1]['extendedIngredients'][j]
        data['results'][-1]['ingredients'].append((lst['name'], lst['measures']['us']['amount'], lst['measures']['us']['unitShort']))


# print(data)
print(js['results'][0])


# In[4]:


import requests
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
# import secret

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

#     print(f"Best data: {data} \n \n ")

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

    return recommendations, data


# In[9]:


# recomendations, data = get_recs(['spaghetti', 'apples', 'tomatoes', 'tofu', 'bread', 'mushrooms', 'tomato sauce'], 10, 'vegan')
recomendations, data = get_recs(["cheddar cheese", "chicken", "tomatoes", "tortilla chips", "carrots", "green beans", "avocado"], 10)
print(data)
# print(data[0]['nutrition']['ingredients'][0])


# In[6]:


def ratio(recipe, used_ids, name, unit):
    total = 0
    used = 0
    for ingr in recipe['nutrition']['ingredients']:
        for nutrient in ingr['nutrients']:
            if nutrient['name'] == name and nutrient['unit'] == unit:
                total+=nutrient['amount']
                used+=nutrient['amount']*(ingr['id'] in used_ids)
                break
                    
    try:
        ratio = used/total
    except:
        ratio = 0.5
    return ratio

def nums(recipe):
    # Create set of used ids
    used_ids = set()
    for ingr in recipe['usedIngredients']:
        used_ids.add(ingr['id'])
       
    num_used_essential, num_missing_essential = get_essentials_info(recipe)
    num_used_noness = recipe['usedIngredientCount'] - num_used_essential
    num_missed_noness = recipe['missedIngredientCount'] - num_missing_essential
    ratio_protein = ratio(recipe, used_ids, 'Protein', 'g')
    ratio_carbs = ratio(recipe, used_ids, 'Carbohydrates', 'g')
    ratio_fat = ratio(recipe, used_ids, 'Fat', 'g')
    ratio_C = ratio(recipe, used_ids, 'Vitamin C', 'mg')
    
    return [num_used_essential, num_missing_essential, num_used_noness, num_missed_noness, ratio_protein, ratio_carbs, ratio_fat, ratio_C]

def numsv(data):
    ret = []
    for recipe in data:
        ret.append(nums(recipe))
    return ret
print(numsv(data))


# In[7]:


import numpy as np
from scipy.stats import norm

class num:   
    def __init__(self, x, e):
        self.x = x
        self.e = np.array(e)
        
    def __add__(self, other):
        if type(other) is num:
            return num(self.x+other.x, self.e+other.e)
        else:
            return num(self.x+other, self.e)
        
    def __sub__(self, other):
        if type(other) is num:
            return num(self.x-other.x, self.e-other.e)
        else:
            return num(self.x-other, self.e)
    
    def __mul__(self, other):
        if type(other) is num:
            return num(self.x*other.x, self.x*other.e + other.x*self.e)
        else:
            return num(self.x*other, self.e*other)
        
    def __truediv__(self, other):
        if type(other) is num:
            return num(self.x/other.x, -other.e*self.x/(other.x**2) + self.e/other.x)
        else:
            return num(self.x/other, self.e/other)
    
    def __neg__(self):
        return num(-self.x, -self.e)

    def __str__(self):
        return f"{self.x} + {self.e}e"
    
def sqrt(self):
    sq = np.sqrt(self.x)
    return num(sq, self.e/(2*sq))

def exp(self):
    ex = np.exp(self.x)
    return num(ex, self.e*ex)

def cdf(self):
    return num(norm.cdf(self.x), norm.pdf(self.x)*self.e)

#rankings = [[1,0],[0,.75,1,.5,.25],...], 0 worst -> 1 best.
def update(vals, rankings, params, step):
    num_params = []
    for i in range(len(params)):
        e = [0]*len(params)
        e[i] = 1
        num_params.append(num(params[i], e))
    
    loss = num(0, [0]*len(params))
    for i in range(len(vals)):
        scores = []
        for j in range(len(vals[i])):
            scores.append(num(0, [0]*len(params)))
            for k in range(len(vals[i][j])):
                scores[-1]+=num_params[k]*vals[i][j][k]
                
        for j in range(len(vals[i])):
            rank = num(0, [0]*len(params))
            for k in range(len(vals[i])):
                if j!=k:
                    rank+=cdf(scores[k]-scores[j])
            rank/=(len(vals[i])-1)
            loss+=(rank - rankings[i][j])*(rank - rankings[i][j])
            
    new_params = []
    for i in range(len(params)):
        new_params.append(params[i]-step*loss.e[i])
    
    return new_params, loss.x

#rankings = [[1,2],[5,2,1,3,4],...], 0 worst -> 1 best.
def find_params(vals, rankings, step, stop):
    for i in range(len(rankings)):
        for j in range(len(rankings[i])):
            rankings[i][j] = (len(rankings[i])-rankings[i][j])/(len(rankings[i])-1)
    loss = 1000000000
    params = [0]*len(vals[0][0])
    while(True):
        params, loss2 = update(vals, rankings, params, step)
        if abs(loss2-loss)<stop:
            return params
        loss = loss2
        
def rank(vals, params):
    rankings = []
    for val in vals:
        scores = []
        for j in range(len(val)):
            scores.append(0)
            for k in range(len(val[j])):
                scores[-1]+=params[k]*val[j][k]
        
        rankings.append([0]*len(val))
        for i, x in enumerate(sorted(range(len(scores)), key=lambda y: scores[y])):
            rankings[-1][x] = i+1
    return rankings


# In[8]:


vals = [[[0,1],[1,2]],[[0,2],[0,0],[1,1],[2,1],[2,0]],[[3,7],[4,0],[1,-1]]]
rankings = [[1,2],[1,2,3,4,5],[1,2,3]]

params = find_params(vals, rankings, 0.1,0.01)

print(params)
print(rank(vals, params))


# In[77]:


inputs = [0,0.1,0.8,0.4,0.3]
output = [0] * len(inputs)
for i, x in enumerate(sorted(range(len(inputs)), key=lambda y: inputs[y])):
    output[x] = i
print(output)


# In[ ]:




