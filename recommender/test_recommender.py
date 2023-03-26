from recommender import get_recs

ingredients = ["salmon", "bread", "tomato"]

recs = get_recs(ingredients, count=5)

print(recs)