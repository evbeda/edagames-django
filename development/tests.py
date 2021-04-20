from django.test import TestCase
from parameterized import parameterized
from .models import Match
from django.utils import timezone


class Tests(TestCase):
    @parameterized.expand([
        ['bot1', 'bot2', 10, 11, timezone.now()],
        ['bot3', 'bot4', 20, 41, timezone.now()],
        ['bot5', 'bot6', 1, 0, timezone.now()],
    ])
    def test_create_priority(self, player_one, player_two, scr1, scr2, date):
        match = Match.objects.create(
            player_one=player_one,
            player_two=player_two,
            score_p_one=scr1,
            score_p_two=scr2,
            date=date
        )
        self.assertEqual(match.player_one, player_one)
        self.assertEqual(match.player_two, player_two)
        self.assertEqual(match.score_p_one, scr1)
        self.assertEqual(match.score_p_two, scr2)
