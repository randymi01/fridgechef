node dialogue_state {
    has name;
    can init_wlk_ctx {
        new_wlk_ctx = {
            "intent": null,
            "entities": {},
            "prev_state": null,
            "next_state": null,
            "respond": false
        };
        if ("entities" in visitor.wlk_ctx) {
            // Carry over extracted entities from previous interaction
            new_wlk_ctx["entities"] = visitor.wlk_ctx["entities"];
        }
        visitor.wlk_ctx = new_wlk_ctx;
    }
    can nlu {}
    can process {
        if (visitor.wlk_ctx["prev_state"]): visitor.wlk_ctx["respond"] = true;
        else {
            visitor.wlk_ctx["next_state"] = net.root();
            visitor.wlk_ctx["prev_state"] = here;
        }
    }
    can nlg {}
}

node dialogue_yn:dialogue_state{
    can intent.yn;
    can nlu {
        if (!visitor.wlk_ctx["prev_state"]) {
            visitor.wlk_ctx["intent"] = intent.yn(visitor.input);
        }
    }
    can process {
        if (visitor.wlk_ctx["prev_state"]): visitor.wlk_ctx["respond"] = true;
        else {
            for n in --> {
                if (n.context["answer"] == visitor.wlk_ctx["intent"]){
                    visitor.wlk_ctx["next_state"] = n;
                    break;
                }
            }
            visitor.wlk_ctx["prev_state"] = here;
        }
    }
    can nlg {
        visitor.response = "I can answer a variety of FAQs related to Tesla. What can I help you with?";
    } nlu {
        if (Q)
    }

}


// main graph spawns all the nodes and creates edges
graph main_graph {
    has anchor dialogue_root;

    spawn {
        dialogue_root = spawn node::dialogue_root;

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

        output_recipe = spawn node::dialogue_state(
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
    root {
        // begin at dialogue root
        take --> node::dialogue_root;
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