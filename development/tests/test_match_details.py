from django.contrib.auth import get_user_model
from django.test import TestCase
import json
from unittest.mock import MagicMock
from unittest.mock import patch

from auth_app.models import Bot
from development.models import (
    Match,
    MatchMembers,
)
from development.views import MatchDetailsView

from development.common.match_utils import (
    get_page_logs_for_match,
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


class TestMatchUtils(TestCase):
    @patch('development.server_requests.get_logs')
    def test_should_return_first_log_page(self, mocked_get_logs):
        mocked_get_logs.json.return_value = {
            "details": ['log1', 'log2'],
            "next": 'asdkj1i3182ue9wuq9ejqkw912831'
        }
        first_page_logs = get_page_logs_for_match(
            game_id="klklewdhjasjd1238u1",
            page_token=None
        )

        self.assertEqual(
            first_page_logs,
            {
                "logs": ['log1', 'log2'],
                "next_token": 'asdkj1i3182ue9wuq9ejqkw912831'
            }
        )
