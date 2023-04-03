from recommender import get_recs

ingredients = ["pasta", "sun dried tomatoes", "chicken breast", "parmesan cheese", "ground beef", "red potatoes", "butter"]

recs = get_recs(ingredients, count=1)

print(recs)