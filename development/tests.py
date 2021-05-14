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


class Tests(TestCase):
    @parameterized.expand([
        ['bot1', 'bot2', 10, 11, timezone.now()],
        ['bot3', 'bot4', 20, 41, timezone.now()],
        ['bot5', 'bot6', 1, 0, timezone.now()],
    ])
    def test_create_match(
        self,
        bot_one,
        bot_two,
        scr1,
        scr2,
        date
    ):
        usr_one = User.objects.create(
            email='email',
            username='username'
        )
        usr_two = User.objects.create(
            email='email2',
            username='username2'
        )

        match = Match.objects.create(
            user_one=usr_one,
            user_two=usr_two,
            bot_1=bot_one,
            bot_2=bot_two,
            score_p_1=scr1,
            score_p_2=scr2,
            date_match=date,
            game_id=1
        )
        self.assertEqual(match.bot_1, bot_one)
        self.assertEqual(match.bot_2, bot_two)
        self.assertEqual(match.score_p_1, scr1)
        self.assertEqual(match.score_p_2, scr2)


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
