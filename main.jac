// every node of the conversational graph is an instance of dialogue_state
node dialogue_state {
    has title;
    has message; // message variable defines what will be said when this node is visited
    
    // each node has its own walk context so that the conversation can have a notion of state
    // if the node hasn't been visited before, we should initialize the conversation state with this function
    // will likely need a flag to do this, however for our purposes we may not even need state if we are using a python backend
    can init_wlk_ctx {
        new_wlk_ctx = {
            "intent": null, // what the user types, triggering the transition
            "entities": {}, // TODO: implement entity extractor and put entities here, pass them on when necessary
            "prev_state": null, // the node we were previously at
            "next_state": null, // the node which we will go to
            "respond": false // a flag which signals if we output the message
        };
        visitor.wlk_ctx = new_wlk_ctx;
    }
    can nlu {}
    // process function efines how we transition between graph nodes
    can process {
        // visitor is the walker that moves between nodes
        // when we are at a node, if we have already filled out the context variable
        // (meaning we already visited the node)
        // output the response
        if (visitor.wlk_ctx["prev_state"]): visitor.wlk_ctx["respond"] = true;
        // otherwise set the next state for where we go after we get a response
        // and also set the previous state to prepare for a response
        else {
            visitor.wlk_ctx["next_state"] = -[intent_transition(intent==visitor.wlk_ctx["intent"])]->[0];
            visitor.wlk_ctx["prev_state"] = here;
        }
    }
    can nlg {}
    // call this funciton to print a message
    can print_message {
        std.out(message);
    }
}

node dialogue_yn:dialogue_state{
}

node dialogue_root:dialogue_state{
}

// the node for when we complete the dialogue is the same, except i overwrite the node transition variable to do nothing
node complete:dialogue_state {
    has title="User likes the recipe";
    has message="";
    can process {
        // this throws an error technically, but not sure how else to quit the dialogue.
    }
}

edge intent_transition {
    has intent;
}

// main graph spawns all the nodes and creates edges
graph main_graph {
    has anchor dialogue_root;

    spawn {
        dialogue_root = spawn node::dialogue_root(
            has title = "dialogue_root",
            has message = "Welcome to Fridgechef, is this your first time using the app?"
        );

        dietary_restrictions = spawn node::dialogue_state(
            title="Dietary restrictions",
            message="What dietary restrictions do you have?"
        );

        current_ingredients = spawn node::dialogue_state(
            title="List of current ingredients",
            message="What ingredients do you currently have?"
        );

        preference = spawn node::dialogue_state(
            title="User preferences",
            message="How long do you have to cook?"
        );

        output_recipe = spawn node::dialogue_yn(
            title="Recipe",
            message="Here's the recipe I outputted, do you like it?"
        );

        is_like = spawn node::dialogue_state(
            title="User like recipe or not",
            message="Happy cooking! Type 'exit' to exit"
        );

        dont_like = spawn node::dialogue_state(
            title="User does not like the recipe",
            message="Let me generate another recipe, type anything to continue"
        );

        complete = spawn node::complete;

        // currently to transition between nodes you have to type the exact content of the intent variable
        // with an intent classifier, we can map different inputs to the intent variable options
        dialogue_root +[intent_transition(intent="yes")]+> dietary_restrictions;
        dietary_restrictions +[intent_transition(intent="allergies")]+> current_ingredients;

        dialogue_root +[intent_transition(intent="no")]+> current_ingredients;
        current_ingredients +[intent_transition(intent="ingredients")]+> preference;

        preference +[intent_transition(intent="preferences")]+> output_recipe;
        output_recipe +[intent_transition(intent="yes")]+> is_like;
        is_like +[intent_transition(intent="exit")]+> complete;
        is_like +[intent_transition(intent="no")]+> dont_like;
        dont_like +[intent_transition(intent="okay")]+> output_recipe;
    }
}

// initializes everything
walker init {
    root {
        spawn here ++> graph::main_graph;
        spawn here walker::talk;
    }
}

// the walker that traverses the graph
walker talk {
    has question;
    has wlk_ctx = {};
    has response;
    can intent.yn;
    root {
        // begin at dialogue root
        take --> node::dialogue_root;
    }

    dialogue_yn{
        question = std.input("FridgeChef (Ctrl + C to exit)> ");
        predicted_intent = intent.yn(question);
        visitor.wlk_ctx["intent"] = predicted_intent;
        take visitor.wlk_ctx["next_state"];
    }

    // this triggers everytime we traverse a node of type "dialogue state"
    dialogue_state {
        // first, if a response (question variable) hasn't been defined, prompt input and set intent variable
        if (!question) {
            here::init_wlk_ctx;
            question = std.input("FridgeChef (Ctrl + C to exit)> ");
            visitor.wlk_ctx["intent"] = question;
        }
        // process the response to figure out what node to transition to next
        here::process;
        // if the "respond" variable is set, output the response and erase the question, then go to next state
        if (visitor.wlk_ctx["respond"]) {
            here::nlg;
            here::print_message;
            question = null;
            take visitor.wlk_ctx["next_state"];
        } else {
            take visitor.wlk_ctx["next_state"] else: take here;
        }
    }
}