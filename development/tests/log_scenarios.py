
from development.constants import INVALID_STATE, VALID_STATE


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
        'current_player': 'any'}
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
        'current_player': ''}
    for replace_value in values_to_update:
        mocked_response.update(replace_value)
    return mocked_response


logs_test_for_validating_moves_0 = [
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


logs_test_for_validating_moves_1 = [
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

logs_test_for_validating_moves_2 = [
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


logs_test_for_validating_moves_3 = [
    mocked_user_action(),

]
