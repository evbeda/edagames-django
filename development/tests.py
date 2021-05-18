from parameterized import parameterized
from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from .forms import (
    get_users_data,
    get_my_bots,
    get_online_bots,
)
from .models import Match
from auth_app.models import (
    Bot,
    User,
)
from .serializer import MatchSerializer


class Tests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        self.bot1 = Bot.objects.create(name='bot1', user=self.user1)
        self.user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        self.bot2 = Bot.objects.create(name='bot2', user=self.user2)

    def test_create_match(self):
        data = {
            'game_id': '1111',
            'bot_1': self.bot1.id,
            'score_p_1': 2000,
            'user_1': self.user1.id,
            'bot_2': self.bot2.id,
            'score_p_2': 1000,
            'user_2': self.user2.id
        }
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        match = Match.objects.filter(game_id='1111')[0]
        self.assertEqual(match.bot_1, self.bot1)
        self.assertEqual(match.bot_2, self.bot2)
        self.assertEqual(match.score_p_1, 2000)
        self.assertEqual(match.score_p_2, 1000)
        self.assertEqual(match.user_1, self.user1)
        self.assertEqual(match.user_2, self.user2)


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
