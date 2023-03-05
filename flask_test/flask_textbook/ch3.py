# Views handle two types of logic (backend and frontend)
# moving frontend to "templates" folder improves readability

# template is a file that containts the html of a response
# elements from the backend can be added dynamically to the
# response via rendering which is done by the Jinja2 template engine

# render_template is jinja2 rendering engine
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):

    # values used by the render template are passed as key,value pairs
    # value can be anything: function, iterable...
    return render_template('user.html', NAME = name,
                           HTML = '<p>Here is not malicious code</p>')

# apply conditional statements and for loop to display the nth recipe
import json
with open("../recipe_book.json",'r') as f:
    recipe_book = json.load(f)

num_recipes = len(recipe_book)

# be able
def format_price(money: str):
    return "$"+money

def dict_html_printer(recipe):
    return_string = ""
    for key,value in recipe.items():
        return_string += f"<li> {key}: {value}</li>"
    return return_string
        

@app.route('/recipes/<recipe_num>')
def recipes(recipe_num):
    if int(recipe_num) > num_recipes:
        return render_template("404.html")  #could also add a 404 here as a response code
    else:
        return render_template("recipes.html", RECIPE = recipe_book[int(recipe_num)], DICT_PRINTER = dict_html_printer, NUM = recipe_num,
                               MONEY_FUNC = format_price)


if __name__ == '__main__':
    # webpage updates as script updates
    app.run(debug=True)
