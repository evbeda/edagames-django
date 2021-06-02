from django.test import TestCase
from django.contrib.auth import get_user_model
from development.models import Match
from development.views import MatchDetailsView
from auth_app.models import Bot
from tournaments.models import Tournament
from unittest.mock import patch
from unittest.mock import MagicMock
import json


class TestMatchDetailsView(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create_user(
            "test_user1",
            "test_user1@email.com",
            "my_pass",
        )
        self.client.force_login(self.user1)
        self.tournament = Tournament.objects.create(
            name='test_tournament',
        )
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
            tournament_id=self.tournament,
            user_1=self.user1,
            user_2=self.user2,
            bot_1=self.bot1,
            bot_2=self.bot2,
            score_p_1=100,
            score_p_2=200,
            game_id='test_game_id'
        )

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

    def test_shloud_instance_a_match_details_view_properly(self):
        view = MatchDetailsView()
        self.assertEqual(view.prev_page, 1)
        self.assertEqual(view.next_page, 2)

    @patch('development.views.get_logs')
    def test_should_shows_matches_if_connected_user_has_matches_played(
        self,
        mocked_get_log,
    ):
        response = self.client.get(f'/match_details/{self.user1.id}?page=1')
        self.assertEquals(response.context_data['object'].id, self.match.id)

    @patch('development.views.get_logs')
    def test_should_shows_pass_data_to_template_when_it_is_received_from_server(
        self,
        mocked_get_log,
    ):
        mocked_response = MagicMock(json=lambda: json.loads('{"details": "testing"}'), spec=["json"])
        mocked_get_log.return_value = mocked_response
        response = self.client.get(f'/match_details/{self.user1.id}?page=1')
        self.assertEquals(
            response.context_data['data'],
            'testing'
        )
