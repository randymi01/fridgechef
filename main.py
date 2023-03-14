import numpy as np
import intent_classification.yn

class node:
    def __init__(self, prompt: str):
        self.child = None
        self._prompt = prompt
        self._response = None

    # instatiated before runtime
    def add_child(self, child):
        self.child = child
    
    def get_child(self):
        return self.children[0]

    def prompt(self):
        self._response = input(self._prompt)

    def actions(self):
        prompt(self)


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
        return self.children[get_intent()]

    def get_intent(self):
        intent = self.intent_func(self._response)
        if intent in self.children.keys():
            return intent
        else:
            raise Exception(f"Intent \"{intent}\" not found")
            pass
    def actions(self):
        prompt(self)

class walker:
    def __init__(self, root):
        self.current = root
        self.end_flag = False
    def traverse(self):
        while not self.end_flag:
            self.current.action()
            self.current = self.current.get_child()
            if self.current == None:
                self.end_flag = True


n0_start = node("Hello, Welcome to FridgeChef")
n1_first_time = node("Is this your first time using FridgeChef?")
n2_dietary_restrictions = node("Do you have any dietary restrictions?")
n3_ingredients = node("What ingredients do you have?")
n4_preference = node("Do you have a cuisine preference?")

# probably wanna make this an output node type
n5_output_recipe = node("Here is your recipe:")

n6_like_recipe = node("Do you like this recipe?")
n7_yes = node("Great!")
n8_no = node("Sorry, we will try again")

