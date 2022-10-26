from django.test import TestCase
from parameterized import parameterized

from development.common.logs_utils import FilterLogs
from development.constants import (
    ALL_ACTIONS,
    ALL_STATES,
    INVALID_STATE,
    MOVE_ACTION,
    SHOOT_ACTION,
    VALID_STATE,
    WALL_ACTION,
)
from development.tests.log_scenarios import (
    logs_test_for_kind_of_move_action,
    logs_test_for_kind_of_shoot_action,
    logs_test_for_kind_of_move_and_shoot_actions,
    logs_test_for_kind_of_move_shoot_and_wall_actions,
    logs_test_for_kind_of_move_without_actions,
    logs_test_for_validating_moves_only_valid_states,
    logs_test_for_validating_moves_valid_and_invalid_state,
    logs_test_for_validating_moves_only_invalid_states,
    logs_test_for_validating_moves_without_log_state,
)


class TestFilterLogs(TestCase):

    @parameterized.expand([
        (logs_test_for_validating_moves_only_valid_states,),
        (logs_test_for_validating_moves_valid_and_invalid_state,),
        (logs_test_for_validating_moves_only_invalid_states,),
        (logs_test_for_validating_moves_without_log_state,),
    ])
    def test_correct_FilterLogs_intance_creation(self, data):
        filter_logs = FilterLogs(data)
        self.assertEqual(filter_logs.logs, data)

    @parameterized.expand([
        (logs_test_for_validating_moves_only_valid_states, [VALID_STATE, ALL_STATES]),
        (logs_test_for_validating_moves_valid_and_invalid_state, [VALID_STATE, INVALID_STATE, ALL_STATES]),
        (logs_test_for_validating_moves_only_invalid_states, [INVALID_STATE, ALL_STATES]),
        (logs_test_for_validating_moves_without_log_state, [ALL_STATES]),
    ])
    def test_getting_possible_log_actions_states(self, data, expected_possible_states):
        possible_states = FilterLogs(data).possible_states
        self.assertEqual(
            sorted(possible_states),
            sorted(expected_possible_states)
        )

    @parameterized.expand([
        (logs_test_for_kind_of_move_action, [MOVE_ACTION, ALL_ACTIONS]),
        (logs_test_for_kind_of_shoot_action, [SHOOT_ACTION, ALL_ACTIONS]),
        (logs_test_for_kind_of_move_and_shoot_actions, [MOVE_ACTION, SHOOT_ACTION, ALL_ACTIONS]),
        (logs_test_for_kind_of_move_shoot_and_wall_actions, [MOVE_ACTION, SHOOT_ACTION, WALL_ACTION, ALL_ACTIONS]),
        (logs_test_for_kind_of_move_without_actions, [ALL_ACTIONS]),
    ])
    def test_getting_possible_log_action(self, data, expected_possible_actions):
        possible_actions = FilterLogs(data).possible_actions
        self.assertEqual(
            sorted(possible_actions),
            sorted(expected_possible_actions)
        )
