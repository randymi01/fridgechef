import numpy as np
import intent_classification.yn as yn
import entity_extraction.food_extractor as food_extractor
import json

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
        self._response = input("\n"+self._prompt + ": ")

    def get_response(self):
        return self._response

    def actions(self):
        self.prompt()

class output_node(node):
    def prompt(self):
        print("\n"+self._prompt)

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


class walker:
    def __init__(self, root, json_path):
        self.current = root
        self.end_flag = False
        self.json_path = json_path
        self.node_number = 0
        self.json_obj = {"responses":[], "entities":{}, "length":0}
    def traverse(self):
        while not self.end_flag:
            self.current.actions()
            self.json_obj["responses"].append(self.current.get_response())
            if isinstance(self.current, entity_extraction_node):
                self.json_obj["entities"][self.current.entity_name] = self.current.get_entity()
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
n2_dietary_restrictions = node("Do you have any dietary restrictions?")
n3_ingredients = entity_extraction_node("What ingredients do you have?",food_extractor.food_extractor, "ingredients")
n4_preference = node("Do you have a cuisine preference? (leave blank if no preference)")

# probably wanna make this an output node type
n5_output_recipe = output_node("Here is your recipe")

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

w = walker(n0_start, "conversations/output.json")
w.traverse()
