from recommender import get_recs

ingredients = ["chicken", "tortilla", "tomatoes", "cheese", "salmon", "bread", "pork", "rice", "noodles"]

recs = get_recs(ingredients)

print(recs['results'])