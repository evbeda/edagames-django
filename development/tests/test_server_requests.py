from django.test import TestCase
from unittest.mock import patch
from development.server_requests import (
    get_logs,
    send_challenge,
)


def mocked_requests_get(*args, **kwargs):
    data = dict()
    for key, value in zip(kwargs['keys'], kwargs['values']):
        data[key] = value

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(data, 200)


class TestServerRequests(TestCase):

    @patch(
        'requests.get',
        side_effect=lambda x: mocked_requests_get(
        ),
    )
    def test_send_challenge(self):
        self.assertEqual(
            send_challenge(
                challenger="test_challenger",
                challenged=["test_challenged"],
                tournament_id="",
            ).status_code,
            200,
        )
