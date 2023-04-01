from recommender import get_recs

ingredients = ["pasta", "tomatoes", "chicken", "parmesan cheese", "beef"]

recs = get_recs(ingredients, count=1)

print(recs)