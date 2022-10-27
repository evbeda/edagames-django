from unittest.mock import (
    patch,
    PropertyMock,
)

from django.contrib.auth import get_user_model
from django.test import TestCase
from parameterized import parameterized

from auth_app.models import Bot
from development.common.logs_utils import FilterLogs
from development.constants import (
    ALL_ACTIONS,
    ALL_STATES,
    INVALID_STATE,
    MOVE_ACTION,
    SHOOT_ACTION,
    VALID_STATE,
)
from development.models import (
    Match,
    MatchMembers,
)


class TestMatchDetailsView(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create_user(
            "test_user1",
            "test_user1@email.com",
            "my_pass",
        )
        self.client.force_login(self.user1)
        self.user2 = get_user_model().objects.create_user(
            "test_user2",
            "test_user2@email.com",
            "my_pass2",
        )
        self.bot1 = Bot.objects.create(
            name='test_bot1',
            user=self.user1,
        )
        self.bot2 = Bot.objects.create(
            name='test_bot2',
            user=self.user2,
        )
        self.match = Match.objects.create(
            tournament_id=None,
            game_id='test_game_id',
        )
        match_members = [
            MatchMembers(
                bot=self.bot1,
                score=500,
                match=self.match,
            ),
            MatchMembers(
                bot=self.bot2,
                score=1000,
                match=self.match,
            )
        ]
        MatchMembers.objects.bulk_create(match_members)

    @patch('development.views.get_logs')
    def test_should_return_200_when_user1_makes_a_request_for_one_of_his_matches(
        self,
        mocked_get_log,
    ):
        response = self.client.get(f'/match_details/{self.user1.id}?page=1')
        self.assertEqual(
            response.status_code,
            200,
        )

    @patch('development.views.get_logs')
    def test_should_use_match_details_template_when_user_makes_a_request(
        self,
        mocked_get_log,
    ):
        response = self.client.get(f'/match_details/{self.user1.id}?page=1')
        self.assertTemplateUsed(
            response,
            'development/match_details.html',
        )

    @patch('development.views.get_logs')
    def test_should_shows_matches_if_connected_user_has_matches_played(
        self,
        mocked_get_log,
    ):
        response = self.client.get(f'/match_details/{self.user1.id}?page=1')
        self.assertEquals(response.context_data['object'].id, self.match.id)

    @patch('development.views.get_logs')
    @patch('development.views.generate_text')
    @patch.object(FilterLogs, 'possible_states', new_callable=PropertyMock)
    @patch.object(FilterLogs, 'possible_actions', new_callable=PropertyMock)
    def test_should_shows_pass_data_to_template_when_it_is_received_from_server(
        self,
        mocked_possible_action,
        mocked_possible_states,
        mocked_generate_text,
        mocked_get_log,
    ):
        return_value = {
            "details": "testing",
            "prev": None,
            "next": "asdqweu12391823uiwjkdnsamd"
        }
        return_value = {
            "details": "testing",
            "prev": None,
            "next": "asdqweu12391823uiwjkdnsamd"
        }

        mocked_get_log.return_value = return_value
        mocked_generate_text.return_value = return_value

        response = self.client.get(f'/match_details/{self.user1.id}?page=1')
        self.assertEquals(
            response.context_data['data'],
            "testing"
        )

    @patch('development.views.get_logs')
    @patch('development.views.generate_text')
    @patch.object(FilterLogs, 'possible_states', new_callable=PropertyMock)
    @patch.object(FilterLogs, 'possible_actions', new_callable=PropertyMock)
    def test_should_shows_pass_data_to_template_when_it_is_received_from_server_in_new_match(
        self,
        mocked_possible_action,
        mocked_possible_states,
        mocked_get_log,
        mocked_generate_text,
    ):
        return_value = {
            "details": "testing",
            "prev": None,
            "next": "asdqweu12391823uiwjkdnsamd"
        }
        return_value = {
            "details": "testing",
            "prev": None,
            "next": "asdqweu12391823uiwjkdnsamd"
        }
        mocked_get_log.return_value = return_value
        mocked_generate_text.return_value = return_value
        response = self.client.get(f'/new_match_details/{self.user1.id}?page=1')
        self.assertEquals(
            response.context_data['data'],
            "testing"
        )

    @parameterized.expand([
        ([INVALID_STATE, VALID_STATE, ALL_STATES], [ALL_ACTIONS],),
        ([VALID_STATE, ALL_STATES], [MOVE_ACTION, SHOOT_ACTION, ALL_ACTIONS],),
    ])
    @patch('development.views.get_logs')
    @patch('development.views.generate_text')
    @patch.object(FilterLogs, 'possible_states', new_callable=PropertyMock)
    @patch.object(FilterLogs, 'possible_actions', new_callable=PropertyMock)
    def test_should_shows_filter_logs_options_to_template_when_it_is_received_from_server(
        self,
        possible_states,
        possible_actions,
        mocked_possible_action,
        mocked_possible_states,
        mocked_generate_text,
        mocked_get_log,
    ):

        mocked_possible_action.return_value = possible_actions
        mocked_possible_states.return_value = possible_states

        response = self.client.get(f'/match_details/{self.user1.id}?page=1')

        self.assertEquals(
            response.context_data['move_states'],
            possible_states
        )
        self.assertEquals(
            response.context_data['actions_kind'],
            possible_actions
        )
