node dialogue_root;
node dialogue_state {
    has title;
    has message;
}

edge intent_transition {
    has intent;
}

node first_time:dialogue_state {
    has name = "first_time";
    can nlg {
        visitor.response = "You can order a Tesla through our design studio";
    }
}

graph main_graph {
    has anchor dialogue_root;

    spawn {
        dialogue_root = spawn node::dialogue_root;

        first_time = spawn node::dialogue_state(
            title="First time user",
            message="Welcome to Fridgechef, is this your first time using the app?"
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

        output_recipe = spawn node::dialogue_state(
            title="Recipe",
            message="Here's the recipe I outputted"
        );

        is_like = spawn node::dialogue_state(
            title="User like recipe or not",
            message="Do you like this recipe?"
        );

        dont_like = spawn node::dialogue_state(
            title="User does not like the recipe",
            message="Let me generate another recipe"
        );

        complete = spawn node::dialogue_state(
            title="User likes the recipe",
            message="Happy cooking!"
        );

        dialogue_root ++> first_time;
        first_time ++> dietary_restrictions;
        dietary_restrictions ++> current_ingredients;
        first_time ++> current_ingredients;
        current_ingredients ++> preference;
        preference ++> output_recipe;
        output_recipe ++> is_like;
        is_like ++> complete;
        is_like ++> dont_like;
        dont_like ++> output_recipe;
    }
}

walker init {
    can calculator.add;
    report calculator.add(1,1);
    root  {
        spawn here ++> graph::main_graph;
    }
}