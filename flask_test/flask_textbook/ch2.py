from flask import Flask

# encapsulates user HTTP request (global context)
# Each time a user connects, a new request is made
from flask import request

# Flask has a number of globals
# 1. Application Context
#   a. current_app -> application instance
#   b. g -> temp storage meant to reset with each request
# 2. Request Context
#   a. request
#   b. session -> disctionary of values that are remembered between requests

app = Flask(__name__)

# CHAPTER 2: FLASK URLS, Context, Responses

# route is associated url
# default root is '/' (uses decorator notation)
@app.route('/')
def index():
    # response is the return value
    # simple functions that return html are called view functions

    # user_agent gets attribute from user HTTPS request represented by global variable "request"
    user_agent = request.headers.get('User-Agent')
    return '<h1> hi </h1>' + '</br>' + '<h1> Browser: {} </h1>'.format(user_agent), 200 # response code

from flask import make_response
@app.route('/cookie')
def cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')

    # returning response instead of html is functionally the same except
    # can use response funcs like set_cookie
    return response, 200


# Flask special responses

from flask import redirect
@app.route('/redirect')
def redirect():
    return redirect('http://www.google.com')

from flask import abort

# String formatting in URLS
# name variable is dynamic (<>) with url below
# name is passed to view function
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    # webpage updates as script updates
    app.run(debug=True)

    # check URL map
        # from main import app
        # app.url_map


# forgot how decorators work
"""
def func_wrapper(func, times):
    for i in range(times):
        func()

@func_wrapper(10)
def print_yes():
    print("yes")

print_yes()
"""

