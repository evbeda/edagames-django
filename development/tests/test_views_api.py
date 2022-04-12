import json
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from parameterized import parameterized

from auth_app.models import (
    Bot,
    User,
)
from development.models import (
    Match,
    MatchMembers,
)
from development.common.match_utils import save_match
from development.views_api import match_list


class Tests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=False)
        self.user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        self.bot1 = Bot.objects.create(name='bot_1', user=self.user1)
        self.user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        self.bot2 = Bot.objects.create(name='bot_2', user=self.user2)

    @parameterized.expand([
        (
            '2players',
            {
                'game_id': '1111',
                'tournament_id': None,
                'data': [
                    ['bot_1', 2000],
                    ['bot_2', 123],
                ]
            },
        ),
        (
            '4players',
            {
                'game_id': '1111',
                'tournament_id': '',
                'data': [
                    ['bot_1', 2000],
                    ['bot_2', 123],
                    ['bot_3', 432],
                    ['bot_4', 999],
                ]
            },
        ),
    ])
    @patch('development.views_api.save_match')
    def test_match_list_should_call_save_match_when_validated_data_is_OK(
        self,
        _test_name,
        match_info,
        mock_save_match,
    ):
        request = self.factory.post('match/', json.dumps(match_info), content_type='application/json')
        match_list(request)
        mock_save_match.assert_called_once_with(match_info)

    @patch('development.views_api.save_match')
    def test_match_list_should_NOT_call_save_match_when_validated_data_is_WRONG(
        self,
        mock_save_match,
    ):
        match_info = {
            'games_id': '2222',
            'tournament_id': '',
            'data': [
                ['bot_1', 555],
                ['bot_2', 123],
            ]
        }
        request = self.factory.post('match/', json.dumps(match_info), content_type='application/json')
        match_list(request)
        mock_save_match.assert_not_called()

    def test_save_match_should_store_a_match_and_associate_members_to_it(self):
        match_info = {
            'game_id': '2222',
            'tournament_id': '',
            'data': [
                ['bot_1', 555],
                ['bot_2', 123],
            ]
        }
        save_match(match_info)
        match = Match.objects.get(game_id=match_info['game_id'])
        match_members = list(MatchMembers.objects.filter(match=match))
        self.assertTrue(match)
        match_members_expected = [
            MatchMembers(
                id=1,
                score=2000,
                bot=self.bot1,
                match=match,
            ),
            MatchMembers(
                id=2,
                score=123,
                bot=self.bot2,
                match=match,
            ),
        ]
        self.assertEqual(
            match_members,
            match_members_expected,
        )

    @parameterized.expand([
        (
            'data_ok',
            {
                'game_id': '2222',
                'tournament_id': '',
                'data': [
                    ['bot_1', 555],
                    ['bot_2', 123],
                ]
            },
            201,
        ),
        (
            'data_wrong',
            {
                'asdasd': '2222',
                'tournament_id': '',
                'data': [
                    ['bot_1', 555],
                    ['bot_2', 123],
                ]
            },
            400,
        ),
    ])
    def test_should_return_status_expected_when_data_from_server_is_received(
        self,
        _test_name,
        match_info,
        status_expected,
    ):
        request = self.factory.post('match/', json.dumps(match_info), content_type='application/json')
        response = match_list(request)
        self.assertEqual(
            response.status_code,
            status_expected,
        )
