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

