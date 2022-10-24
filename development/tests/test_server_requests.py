import json
from unittest.mock import (
    MagicMock,
    patch,
)

from django.test import TestCase
from parameterized import parameterized

from development.server_requests import (
    get_logs,
    send_challenge,
)
from edagames.settings import (
    SERVER_PORT,
    SERVER_URL,
)


class TestServerRequests(TestCase):

    @parameterized.expand(
        [
            ('debug_mode_enable', True, ),
            ('debug_mode_disable', False, ),
        ]
    )
    def test_send_challenge(self, name, debug_mode):
        test_player1 = 'test_player1'
        test_player2 = ['test_player2']
        debug_mode = debug_mode
        mocked_response = MagicMock(json=lambda x: json.loads(x), spec=["json"])
        with patch(
            'requests.post',
            return_value=mocked_response,
        ) as request_get_mocked:
            send_challenge(
                test_player1,
                test_player2,
                debug_mode=debug_mode,
            )
            request_get_mocked.assert_called_once_with(
                f'{SERVER_URL}:{SERVER_PORT}/challenge',
                json={
                    'challenger': test_player1,
                    'challenged': test_player2,
                    'tournament_id': '',
                    'debug_mode': debug_mode,
                }
            )

    def test_get_logs(self):
        game_id = 'test_game_id'
        page_token = None
        mocked_response = json.dumps({
            "details": "testing",
            "prev": None,
            "next": "asdqweu12391823uiwjkdnsamd"
        })
        with patch(
            'requests.get',
        ) as request_get_mocked:
            request_get_mocked.json = mocked_response
            get_logs(
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
