from recommender import get_recs

ingredients = ["chicken", "bread", "tomato", "cheese"]

recs = get_recs(ingredients, count=2)

print(recs)