import json
with open("../recipe_book.json",'r') as f:
    recipe_book = json.load(f)

for key,value in recipe_book[1].items():
    print(f"{key}: {value}")
    print('\n')