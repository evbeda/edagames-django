from development.constants import (
    ACTION,
    INVALID_STATE,
    MOVE_ACTION,
    SHOOT_ACTION,
    VALID_STATE,
    WALL_ACTION,
)


def mocked_user_action(values_to_update=[]) -> dict:
    mocked_action = {
        'action': 'any_action',
        'data': {
            "from_row": 0,
            "from_col": 0,
            "direction": "any",
            "game_id": "",
            "turn_token": "aaaaa"
        },
        'current_player': 'any',
    }
    for replace_value in values_to_update:
        mocked_action.update(replace_value)
    return mocked_action


def mocked_game_response(values_to_update=[]) -> dict:
    mocked_response = {
        'game_id': 'xyz',
        'board': 'xxaxaxaxa',
        'remaining_turns': 'aaaaa',
        'state': 'valid',
        'score_1': '',
        'direction': '',
        'score_2': '',
        'arrows_1': '5',
        'arrows_2': '',
        'player_1': '',
        'player_2': '',
        'side': '',
        'from_row': '',
        'from_col': '',
        'current_player': '',
    }
    for replace_value in values_to_update:
        mocked_response.update(replace_value)
    return mocked_response


logs_test_for_validating_moves_only_valid_states = [
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
]


logs_test_for_validating_moves_valid_and_invalid_state = [
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': VALID_STATE}]),
    mocked_user_action(),
]

logs_test_for_validating_moves_only_invalid_states = [
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
    mocked_game_response([{'state': INVALID_STATE}]),
    mocked_user_action(),
]


logs_test_for_validating_moves_without_log_state = [
    mocked_user_action(),
]


logs_test_for_kind_of_move_action = [
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
]

logs_test_for_kind_of_shoot_action = [
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
]


logs_test_for_kind_of_move_and_shoot_actions = [
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
]

logs_test_for_kind_of_move_shoot_and_wall_actions = [
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: MOVE_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: SHOOT_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: WALL_ACTION}]),
    mocked_game_response(),
    mocked_user_action([{ACTION: WALL_ACTION}]),
]


logs_test_for_kind_of_move_without_actions = [
    mocked_game_response(),
    mocked_game_response(),
    mocked_game_response(),
]
