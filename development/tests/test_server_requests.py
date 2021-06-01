from django.test import TestCase
from unittest.mock import patch
from development.server_requests import (
    get_logs,
    send_challenge,
)
import json
from unittest.mock import MagicMock


class TestServerRequests(TestCase):

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
                'http://127.0.0.1:5000/challenge',
                json={
                    'challenger': test_player1,
                    'challenged': test_player2,
                    'tournament_id': '',
                }
            )

    def test_get_logs(self):
        game_id = 'test_game_id'
        page_token = None
        mocked_response = MagicMock(json=lambda x: json.loads(x), spec=["json"])
        with patch(
            'requests.get',
            return_value=mocked_response,
        ) as request_get_mocked:
            get_logs(
                game_id,
                page_token,
            )
            request_get_mocked.assert_called_once_with(
                'http://127.0.0.1:5000/match_details',
                params={
                    'game_id': game_id,
                    'page_token': page_token,
                }
            )
