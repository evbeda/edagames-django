from django.test import TestCase

from auth_app.models import (
    Bot,
    User,
)
from development.common.match_utils import (
    calculate_match_result,
    generate_match_members,
)
from development.models import Match


class TestMatchUtils(TestCase):
    def test_should_calculate_the_match_result_one_winner(self):
        match_data = [
            ['bot_2', 123],
            ['bot_1', 555],
            ['bot_3', 441],
            ['bot_5', 324],
        ]
        match_result = calculate_match_result(match_data)
        self.assertEqual(match_result["winner"], 'bot_1')
        self.assertEqual(match_result["ties"], [])

    def test_should_return_one_winner_but_no_ties_even_there_are_ties(self):
        match_data = [
            ['bot_2', 333],
            ['bot_1', 555],
            ['bot_3', 333],
            ['bot_5', 333],
        ]
        match_result = calculate_match_result(match_data)
        self.assertEqual(match_result["winner"], 'bot_1')
        self.assertEqual(match_result["ties"], [])

    def test_should_calculate_the_match_result_all_ties(self):
        match_data = [
            ['bot_1', 555],
            ['bot_2', 555],
            ['bot_3', 555],
            ['bot_4', 555],
        ]
        match_result = calculate_match_result(match_data)
        self.assertIsNone(match_result["winner"])
        self.assertEqual(
            match_result["ties"],
            [
                'bot_1',
                'bot_2',
                'bot_3',
                'bot_4',
            ]
        )

    def test_should_calculate_the_match_result_not_winner_some_ties(self):
        match_data = [
            ['bot_1', 555],
            ['bot_2', 123],
            ['bot_3', 555],
            ['bot_4', 11],
        ]
        match_result = calculate_match_result(match_data)
        self.assertIsNone(match_result["winner"])
        self.assertEqual(
            match_result["ties"],
            [
                'bot_1',
                'bot_3',
            ]
        )

    def test_should_generate_match_members_one_winner(self):
        user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        Bot.objects.create(name='bot_1', user=user1)
        user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        Bot.objects.create(name='bot_2', user=user2)
        match_info = {
            'game_id': '2222',
            'tournament_id': '',
            'data': [
                ['bot_1', 555],
                ['bot_2', 123],
            ]
        }
        match_result = {
            "winner": 'bot_1',
            "ties": []
        }
        match = Match.objects.create(
            game_id=match_info['game_id'],
            tournament_id=match_info['tournament_id'],
        )
        match_members = generate_match_members(match, match_info["data"], match_result)
        self.assertEqual(match_members[0].bot_id, 1)
        self.assertEqual(match_members[0].match_id, 1)
        self.assertEqual(match_members[0].match_result, 2)
        self.assertEqual(match_members[1].bot_id, 2)
        self.assertEqual(match_members[1].match_id, 1)
        self.assertEqual(match_members[1].match_result, 0)
