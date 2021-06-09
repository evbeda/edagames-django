from django.test import TestCase
from unittest.mock import patch

from ..forms import (
    get_users_data,
    get_my_bots,
    get_online_bots,
)
from auth_app.models import (
    Bot,
    User,
)


def mocked_requests_get(*args, **kwargs):
    key = kwargs['key']
    data = kwargs['data']

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse({key: data}, 200)


class TestBotHandler(TestCase):

    @patch(
        'requests.get',
        side_effect=lambda x: mocked_requests_get(
            key='users',
            data=['Pedro', 'Pablo', 'Juan'],
        ),
    )
    def test_get_users_data_correct_key(self, mock_get):
        self.assertEqual(
            get_users_data(),
            ['Pedro', 'Pablo', 'Juan'],
        )

    @patch(
        'requests.get',
        side_effect=lambda x: mocked_requests_get(
            key='wrong_key',
            data=[],
        ),
    )
    def test_get_users_data_wrong_key(
        self,
        mock_get,
    ):
        self.assertEqual(
            get_users_data(),
            [],
        )

    def test_get_online_bots(self):
        users = ['Pedro', 'Pablo', 'Gabi']
        self.assertEqual(
            list(get_online_bots(users)),
            [
                (0, 'Pedro'),
                (1, 'Pablo'),
                (2, 'Gabi'),
            ],
        )

    def test_get_online_bots_exception_wrong_key(self):
        users = ['Pedro', 'Pablo', 'Gabi']
        self.assertEqual(
            list(get_online_bots(users)),
            [
                (0, 'Pedro'),
                (1, 'Pablo'),
                (2, 'Gabi'),
            ],
        )

    def test_get_my_bots(self):
        user = User.objects.create(
            email='email',
            username='username'
        )
        Bot.objects.create(
            name='bot_name',
            token='asd123',
            user=user,
        )
        online_bots = ['Pedro', 'bot_name', 'Pablo']
        self.assertEqual(
            list(get_my_bots(user, online_bots)),
            [
                (0, 'bot_name')
            ],
        )
