node dialogue_root;
node dialogue_state {
    has name;
    has response;
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

walker init {
    can calculator.add;
    report calculator.add(1,1);
}