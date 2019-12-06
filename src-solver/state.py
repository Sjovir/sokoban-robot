states = []


def add_state(player_position, box_positions):
    state = state_to_string(player_position, box_positions)
    states.append(state)


def is_state_new(player_position, box_position):
    check_state = state_to_string(player_position, box_position)
    if check_state in states:
        return False
    else:
        return True


def state_to_string(player_position, box_positions):
    state = ''
    state += str(player_position) + '-'
    for position in box_positions:
        state += str(position) + ','

    state = state[:-1]
    return state
