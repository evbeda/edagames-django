from django.test import TestCase
from django.contrib.auth import get_user_model
from development.models import Match
from auth_app.models import Bot
from tournaments.models import Tournament


class TestMatchHistoryView(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create_user(
            "test_user1",
            "test_user1@email.com",
            "my_pass",
        )
        self.client.force_login(self.user1)
        self.tournament = Tournament.objects.create(
            name='test_tournament',
        )
        self.user2 = get_user_model().objects.create_user(
            "test_user2",
            "test_user2@email.com",
            "my_pass2",
        )
        self.user3 = get_user_model().objects.create_user(
            "test_user3",
            "test_user3@email.com",
            "my_pass3",
        )
        self.bot1 = Bot.objects.create(
            name='test_bot1',
            user=self.user1,
        )
        self.bot2 = Bot.objects.create(
            name='test_bot2',
            user=self.user2,
        )
        self.match = Match.objects.create(
            tournament_id=self.tournament,
            user_1=self.user1,
            user_2=self.user2,
            bot_1=self.bot1,
            bot_2=self.bot2,
            score_p_1=100,
            score_p_2=200,
            game_id='test_game_id',
        )

    def test_should_return_200_when_user1_makes_a_request(
        self,
    ):
        response = self.client.get('/match_history')
        self.assertEqual(
            response.status_code,
            200,
        )

    def test_should_use_match_history_template_when_user_makes_a_request(self):
        response = self.client.get('/match_history')
        self.assertTemplateUsed(
            response,
            'development/match_history.html',
        )

    def test_should_shows_matches_if_connected_user_has_matches_played(self):
        response = self.client.get('/match_history')
        self.assertEquals({match.id for match in response.context_data['object_list']}, {self.match.id})

    def test_should_dont_shows_matches_if_connected_user_doesnt_have_any_match_played(self):
        self.client.force_login(self.user3)
        response = self.client.get('/match_history')
        self.assertEqual(len(response.context_data['object_list']), 0)
