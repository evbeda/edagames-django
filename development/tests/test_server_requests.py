from django.test import TestCase
from unittest.mock import (
    MagicMock,
    patch,
)
from development.server_requests import (
    get_all_logs,
    get_one_page_logs,
    send_challenge,
)
import json
from edagames.settings import (
    SERVER_PORT,
    SERVER_URL,
)


class TestServerRequests(TestCase):

    def setUp(self):
        self.logs = [
            json.dumps({
                'details': ['first_page'],
                'next': '1',
            }),
            json.dumps({
                'details': ['second_page'],
                'next': '2',
            }),
            json.dumps({
                'details': ['third_page'],
                'next': '3',
            }),
            json.dumps({
                'details': ['last_page'],
                'next': None,
            }),
        ]

    def test_send_challenge(self):
        test_player1 = 'test_player1'
        test_player2 = ['test_player2']
        mocked_response = MagicMock(json=lambda x: json.loads(x), spec=["json"])
        with patch(
            'requests.post',
            return_value=mocked_response,
        ) as request_get_mocked:
            send_challenge(
                test_player1,
                test_player2,
            )
            request_get_mocked.assert_called_once_with(
                f'{SERVER_URL}:{SERVER_PORT}/challenge',
                json={
                    'challenger': test_player1,
                    'challenged': test_player2,
                    'tournament_id': '',
                }
            )

    def test_get_one_page_logs(self):
        game_id = 'test_game_id'
        page_token = None
        mocked_response = MagicMock(json=lambda x: json.loads(x), spec=["json"])
        with patch(
            'requests.get',
            return_value=mocked_response,
        ) as request_get_mocked:
            get_one_page_logs(
                game_id,
                page_token,
            )
            request_get_mocked.assert_called_once_with(
                f'{SERVER_URL}:{SERVER_PORT}/match_details',
                params={
                    'game_id': game_id,
                    'page_token': page_token,
                }
            )

    def test_should_return_all_log_pages_of_a_match_as_a_list(self):
        with patch(
            ('development.server_requests.get_one_page_logs'),
        ) as mocked_get_one_page_logs:
            mocked_get_one_page_logs.side_effect = self .logs
            logs = get_all_logs('game_id')
            self.assertEqual(
                len(logs),
                4,
            )
