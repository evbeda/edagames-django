
from django.test import TestCase
from parameterized import parameterized

from development.common.logs_utils import FilterLogs
from development.constants import (
    ALL_STATES,
    INVALID_STATE,
    VALID_STATE
)
from development.tests.log_scenarios import (
    logs_test_for_validating_moves_0,
    logs_test_for_validating_moves_1,
    logs_test_for_validating_moves_2,
    logs_test_for_validating_moves_3
)


class TestFilterLogs(TestCase):

    @parameterized.expand([
        (logs_test_for_validating_moves_0,),
        (logs_test_for_validating_moves_1,),
        (logs_test_for_validating_moves_2,),
        (logs_test_for_validating_moves_3,),
    ])
    def test_correct_FilterLogs_intance_creation(self, data):

        filter_logs = FilterLogs(data)
        self.assertEqual(filter_logs.logs, data)

    @parameterized.expand([
        (logs_test_for_validating_moves_0, [VALID_STATE, ALL_STATES]),
        (logs_test_for_validating_moves_1, [VALID_STATE, INVALID_STATE, ALL_STATES]),
        (logs_test_for_validating_moves_2, [INVALID_STATE, ALL_STATES]),
        (logs_test_for_validating_moves_3, [ALL_STATES]),
    ])
    def test_getting_possible_log_actions_states(self, data, expected_possible_states):
        possible_states = FilterLogs(data).possible_states
        self.assertEqual(
            sorted(possible_states),
            sorted(expected_possible_states))
