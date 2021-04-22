from django.test import TestCase
from parameterized import parameterized
from .models import Match
from auth_app.models import User
from django.utils import timezone


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
            bot_one=bot_one,
            bot_two=bot_two,
            score_p_one=scr1,
            score_p_two=scr2,
            date_match=date,
            board_id=1
        )
        self.assertEqual(match.bot_one, bot_one)
        self.assertEqual(match.bot_two, bot_two)
        self.assertEqual(match.score_p_one, scr1)
        self.assertEqual(match.score_p_two, scr2)

