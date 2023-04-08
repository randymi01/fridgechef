import numpy as np
import intent_classification.yn as yn
import entity_extraction.food_extractor as food_extractor 
import recommender.recommender as recommender
import json
import entity_extraction.entity_extract as entity_extract
import entity_extraction.cuisine_extract as cuisine_extract
import entity_extraction.diet_extract as diet_extract
import entity_extraction.intolerance_extract as intolerance_extract
import secret as secret
from twilio.rest import Client
import http.server
import socketserver
import socket
from twilio.twiml.messaging_response import MessagingResponse
import threading
from flask import Flask, request
import time
import requests


class node:
    def __init__(self, prompt: str):
        self.child = None
        self._prompt = prompt
        self._response = None

    # instatiated before runtime
    def add_child(self, child):
        self.child = child
    
    def get_child(self):
        return self.child

    def prompt(self):
        global globalResponse
        globalResponse = ''
        # self._response = input("\n"+self._prompt + ": ")
        # api call to get the response
        client = Client(secret.TWILIO_SID, secret.TWILIO_AUTH)

        message = client.messages.create(
        body=self._prompt,
        from_=secret.twilio_number,
        to=secret.my_phone_number
        )
        print (message.body)
        while globalResponse == '':
            time.sleep(1)
        self._response = globalResponse
        globalResponse = ''

    def get_response(self):
        return self._response

    def actions(self):
        self.prompt()

class output_node(node):
    def prompt(self):
        # print("\n"+self._prompt)
        client = Client(secret.TWILIO_SID, secret.TWILIO_AUTH)

        message = client.messages.create(
        body=self._prompt,
        from_=secret.twilio_number,
        to=secret.my_phone_number
        )
        print (message.body)

class recipe_query_node(output_node):
    def __init__(self, prompt: str):
        self.child = None
        self._prompt = prompt
        self._response = None
        self.recipes = None
        self.times_visited = 0
        self.recipes_to_get = 30

    # NOTE FOR LATER: Do we want to print nutrition info also?
    def query(self, entities):
        # once we get cuisine preferences and restrictions, add here
        if self.times_visited == 0:
            ingredients = []
            diet = None
            cuisine_preferences = None
            allergies = None
            intolerances = None
            # uncomment below for final build potentially
            #try:
            if "ingredients" in entities:
                ingredients = entities["ingredients"]
            if "allergies" in entities:
                allergies = entities["allergies"]
            if "diet" in entities:
                diet = entities["diet"]
            if "intolerances" in entities:
                intolerances = entities["intolerances"]
            if "cuisine" in entities:
                cuisine_preferences = entities["cuisine"]
            self.recipes = recommender.get_recs(ingredients, count=self.recipes_to_get, allergies=allergies, diet=diet, intolerances=intolerances, cuisine=cuisine_preferences)
            #except:
            #    print("Error: Fridgechef is not working right now, come back later.")
            #    exit(1)
            self.recipes_to_get = self.recipes['number'] # in case we got less than 10 recipes, change number we have


    def prompt(self):
        # to iterate through different recipes, every time we visit, we increment the index we take the recipe from
        idx = self.times_visited % self.recipes_to_get
        self.times_visited += 1

        recipe_title = self.recipes["results"][idx]["title"]
        recipe_servings = self.recipes['results'][idx]['servings']
        recipe_time = self.recipes['results'][idx]['readyInMinutes']
        recipe_ingredients = self.recipes["results"][idx]['ingredients']
        recipe_instructions = self.recipes['results'][idx]['instructions']

        client = Client(secret.TWILIO_SID, secret.TWILIO_AUTH)
        
        r = ''
        r += "\n" + self._prompt
        print("\n"+self._prompt)
        if recipe_title:
            r += "\n" + recipe_title + "\n" 
            print("\n"+recipe_title)
        if recipe_servings:
            r += str(recipe_servings) + " servings\n"
            print(str(recipe_servings) + " servings")
        # if recipe time is greater than an hour, print the number of hours and minutes
        if int(recipe_time / 60) > 0:
            r += str(int(recipe_time / 60)) + " hours " + str(recipe_time % 60) + " minutes\n\n"
            print(str(int(recipe_time / 60)) + " hours " + str(recipe_time % 60) + " minutes\n")
        else:
            r += str(recipe_time % 60) + " minutes\n\n"
            print(str(recipe_time % 60) + " minutes\n")

        message = client.messages.create(
        body=r,
        from_=secret.twilio_number,
        to=secret.my_phone_number
        )
        r = ""
        for item in recipe_ingredients:
            # prints num, unit, item, so like "2 tablespoons soy sauce"
            if item[0] and item[1] and item[2]:
                r += str(item[1]) + " " + item[2] + " " + item[0] + "\n"
                print(str(item[1]) + " " + item[2] + " " + item[0])
            # if units not provided, then just like "2 oranges"
            elif item[0] and item[1]:
                r += str(item[1]) + " " + item[0] + "\n"
                print(str(item[1]) + " " + item[0])
            # if quantity not provided, then just like "chocolate"
            elif item[0]:
                r += str(item[0]) + "\n"
                print(str(item[0]))

        message = client.messages.create(
        body=r,
        from_=secret.twilio_number,
        to=secret.my_phone_number
        )
        # newline to separate ingredients from recipes
        r = ""
        print()
        for num, line in enumerate(recipe_instructions):
            # prints numbered instructions, so like "1. boil water"
            r += str(num + 1) + ". " + line + "\n"
            print(str(num + 1) + ". " + line)
            message = client.messages.create(
            body=r,
            from_=secret.twilio_number,
            to=secret.my_phone_number
            )
            r = ""

        

        


class intent_node(node):
    def __init__(self, prompt: str, intent_func):
        self._prompt = prompt
        self._response = None
        self.intent_func = intent_func
        self.children = {}

    # instatiated before runtime
    def add_child(self, child, intent_label: str):
        self.children[intent_label] = child

    def get_child(self):
        return self.children[self.get_intent()]

    def get_intent(self):
        intent = self.intent_func(self._response)
        if intent in self.children.keys():
            return intent
        else:
            raise Exception(f"Intent \"{intent}\" not found")
            pass
    def actions(self):
        self.prompt()

class entity_extraction_node(node):
    def __init__(self, prompt: str, extraction_func, entity_name):
        super().__init__(prompt)
        self.extraction_func = extraction_func
        self.entity_name = entity_name

    # should return entities in list format
    def get_entity(self):
        response = self.extraction_func(self._response)
        if type(response) != list:
            raise Exception(f"Extraction function must return a list of entities")
        else:
            return response
    def actions(self):
        self.prompt()


class dietary_restrictions_node(node):
    def __init__(self, prompt: str):
        super().__init__(prompt)
    
    def get_entity(self):
        dietary_restrictions = []
        dietary_restrictions.append(entity_extract.food_extract(self._response))
        dietary_restrictions.append(diet_extract.diet_extract(self._response))
        dietary_restrictions.append(intolerance_extract.intolerance_extract(self._response))
        for l in dietary_restrictions:
            if type(l) != list:
                raise Exception(f"Extraction function must return a list of entities")
        return dietary_restrictions
    
    def actions(self):
        self.prompt()


class walker:
    def __init__(self, root, json_path):
        self.current = root
        self.end_flag = False
        self.json_path = json_path
        self.node_number = 0
        self.json_obj = {"responses":[], "entities":{}, "length":0}


    def get_entities(self):
        return self.json_obj["entities"]


    def traverse(self):
        while not self.end_flag:
            # perform a query when we reach a recipe query node
            if isinstance(self.current, recipe_query_node):
                self.current.query(self.json_obj["entities"])
            self.current.actions()
            self.json_obj["responses"].append(self.current.get_response())
            if isinstance(self.current, entity_extraction_node):
                self.json_obj["entities"][self.current.entity_name] = self.current.get_entity()
            if isinstance(self.current, dietary_restrictions_node):
                dietary_restrictions = self.current.get_entity()
                self.json_obj["entities"]["allergies"] = dietary_restrictions[0]
                self.json_obj["entities"]["diets"] = dietary_restrictions[1]
                self.json_obj["entities"]["intolerances"] = dietary_restrictions[2]
            self.current = self.current.get_child()
            self.node_number += 1
            if self.current == None:
                self.end_flag = True
                self.json_obj["length"] = self.node_number
        
        # write to json once done
        listobj = []
        with open(self.json_path) as f:
            listobj = json.load(f)
        listobj.append(self.json_obj)
        with open(self.json_path, 'w') as json_file:
            json.dump(listobj, json_file, 
                indent=4,  
                separators=(',',': '))
        



n0_start = output_node("Hello, Welcome to FridgeChef")

n1_first_time = intent_node("Is this your first time using FridgeChef?", yn.yn_intent)

# temporarily using old food extractor for testing
n2_dietary_restrictions = dietary_restrictions_node("Do you have any dietary restrictions? (We will do our best to accomodate)")
n3_ingredients = entity_extraction_node("What ingredients do you have?",food_extractor.food_extractor, "ingredients")

n4_preference = entity_extraction_node("Do you have a cuisine preference?", cuisine_extract.cuisine_extract, "cuisine")

n5_output_recipe = recipe_query_node("Here is your recipe")

n6_like_recipe = intent_node("Do you like this recipe?",yn.yn_intent)
n7_yes = output_node("Great!")
n8_no = output_node("Sorry, we will try again")

n0_start.add_child(n1_first_time)
n1_first_time.add_child(n2_dietary_restrictions, "POSITIVE")
n1_first_time.add_child(n3_ingredients, "NEGATIVE")

n2_dietary_restrictions.add_child(n3_ingredients)
n3_ingredients.add_child(n4_preference)
n4_preference.add_child(n5_output_recipe)
n5_output_recipe.add_child(n6_like_recipe)
n6_like_recipe.add_child(n7_yes, "POSITIVE")
n6_like_recipe.add_child(n8_no, "NEGATIVE")
n8_no.add_child(n5_output_recipe)

app = Flask(__name__)


@app.route('/sms', methods=['POST', 'GET'])
def sms_reply():
    global globalResponse
    # Get the incoming message
    
    globalResponse = request.values.get('Body', None)
    
    # Create a Twilio MessagingResponse object
    resp = MessagingResponse()

    # Add a message to the response
    resp.message(f'You said: {globalResponse}')

    # Return the response as TwiML
    return str(resp)

if __name__ == '__main__':
    global globalResponse
    globalResponse = ''
    # app.run(host='0.0.0.0', port=8000, debug=False)
    t = threading.Thread(target=lambda: app.run(host='localhost', port=8000, debug=False))
    t.start()
    w = walker(n0_start, "conversations/output.json")
    w.traverse()




