from jaseci.actions.live_actions import jaseci_action

@jaseci_action(act_group=["calculator"], allow_remote=True)
def add(first_number: int, second_number: int):
    return first_number + second_number
