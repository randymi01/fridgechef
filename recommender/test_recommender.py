from recommender import get_recs
# First time using
# Lots of allergies
# Strong Cuisine preference
# Picky eater (cycle through several and they are all decent)

# First time - looks good
# ingredients = ["cheddar cheese", "chicken", "tomatoes", "tortilla chips", "carrots", "green beans", "avocado"]
# recs = get_recs(ingredients, count=30)
# print(f"\n \n First time: {recs['results'][0]}")

# Lots of allergies / picky - looks good
# ingredients = ["noodles", "red pepper flakes", "bell pepper", "corn", "tomato", "potato", "garlic", "eggs", "zucchini"]
# recs = get_recs(ingredients, count=30, allergies="Nuts", diet="Vegetarian", intolerances="Peanut,Shellfish", cuisine="Italian")
# print(f"\n \n Allergies: {recs['results'][0]}")

# Picky eater (Chinese) - looks good 
ingredients = ["noodles", "soy sauce", "oyster sauce", "brown rice", "corn", "chicken", "garlic", "eggs", "onion", "scallions", "ginger"]
recs = get_recs(ingredients, count=30, allergies="Nuts", diet=None, intolerances="Peanut,Shellfish", cuisine="Chinese")
print(f"\n \n Allergies (Chinese): {recs['results'][0]}")

# Strong cuisine preference
