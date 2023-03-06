import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from ingredient_parser import parse_ingredient
import requests
import time

ingredients = []


url = "https://www.jamieoliver.com/recipes/category/course/mains/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

recipe_urls = pd.Series([a.get("href") for a in soup.find_all("a")])

recipe_urls = recipe_urls[(recipe_urls.str.count("-")>0)]
recipe_urls = recipe_urls[(recipe_urls.str.contains("/recipes/")==True)]
recipe_urls = recipe_urls[(recipe_urls.str.contains("-recipes/")==True)]
recipe_urls = recipe_urls[(recipe_urls.str.contains("category")==False)]
recipe_urls = recipe_urls[(recipe_urls.str.contains("https")==False)]
recipe_urls = recipe_urls[(recipe_urls.str.endswith("-recipes/")==False)]

for r in recipe_urls:
    r_url = "https://www.jamieoliver.com" + r
    r_soup = BeautifulSoup(requests.get(r_url).content, "html.parser")
    title = r_soup.find("h1").text.strip()

    for ingr in r_soup.select(".ingred-list li"):
        i = " ".join(ingr.text.split())
        parsed_i = parse_ingredient(i)
        ingredients.append(parsed_i["name"])
        print("Original: " + i + " New: " + parsed_i["name"])

    time.sleep(2)

print(ingredients)
    
















    








        



        
    
