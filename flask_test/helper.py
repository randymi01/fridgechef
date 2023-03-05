import pandas as pd
import json
import numpy as np

with open("recipes_with_nutritional_info.json",'r') as f:
    processed = json.load(f)

processed = processed[:100]

def get_ingredients(json_obj : list):
    return np.array([i['text'] for i in json_obj])

test = dict(processed[0])
processed_ids = [i["id"] for i in processed]
processed_title = [i["title"] for i in processed]
processed_ingredients = [get_ingredients(i["ingredients"]) for i in processed]
processed_cals = [round(i["nutr_values_per100g"]["energy"],2) for i in processed]
processed_protein = [round(i["nutr_values_per100g"]["protein"],2) for i in processed]
processed_fat = [round(i["nutr_values_per100g"]["fat"],2) for i in processed]
processed_sugars = [round(i["nutr_values_per100g"]["sugars"],2) for i in processed]

df = pd.DataFrame({"id" : processed_ids, "title": processed_title, "ingredients": processed_ingredients,
                   "cals" : processed_cals, "protein" : processed_protein, "fat" : processed_fat,
                   "sugar" : processed_sugars})

df.to_json("recipe_book.json", orient = "records")