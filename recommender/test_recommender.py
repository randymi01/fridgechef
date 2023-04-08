from recommender import get_recs

ingredients = ["brown rice", "chicken", "steak", "salt", "pepper", "butter", "potato", "corn", "carrots", "tomato", "green beans", "peas"]

recs = get_recs(ingredients, count=4)

print(recs)