from django.contrib.auth import get_user_model
from django.test import TestCase
from parameterized import parameterized

from development.views_api import save_match
from auth_app.models import (
    Bot,
    User,
)
from development.models import (
    Match,
    MatchMembers,
)
from development.views import (
    get_matches_of_connected_user,
    get_matches_results
)


class TestMatchHistoryView(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create_user(
            "test_user1",
            "test_user1@email.com",
            "my_pass",
        )
        self.client.force_login(self.user1)
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
            tournament_id=None,
            game_id='test_game_id',
        )
        match_members = [
            MatchMembers(
                bot=self.bot1,
                score=500,
                match=self.match,
            ),
            MatchMembers(
                bot=self.bot2,
                score=1000,
                match=self.match,
            )
        ]
        MatchMembers.objects.bulk_create(match_members)

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
        self.assertEquals(
            {match_result['match'].id for match_result in response.context_data['object_list']},
            {self.match.id}
        )

    def test_should_dont_shows_matches_if_connected_user_doesnt_have_any_match_played(self):
        self.client.force_login(self.user3)
        response = self.client.get('/match_history')
        self.assertEqual(len(response.context_data['object_list']), 0)


class TestMethodsMatchHistory(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        self.bot1 = Bot.objects.create(name='bot_1', user=self.user1)
        self.user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        self.bot2 = Bot.objects.create(name='bot_2', user=self.user2)
        self.user3 = User.objects.create(email='test3@gmail.com', username='UsuarioTest3')
        self.bot3 = Bot.objects.create(name='bot_3', user=self.user3)
        matches = [
            {'game_id': '1', 'tournament_id': '', 'data': [[self.bot1.name, 1111], [self.bot2.name, 2222]]},
            {'game_id': '2', 'tournament_id': '', 'data': [[self.bot1.name, 1111], [self.bot3.name, 3333]]},
            {'game_id': '3', 'tournament_id': '', 'data': [[self.bot2.name, 2222], [self.bot3.name, 3333]]},
        ]
        for match in matches:
            save_match(match)

    @parameterized.expand([
        ('UsuarioTest1', [1, 2]),   # match(1)bot1 vs bot2, match(2)bot1 vs bot3
        ('UsuarioTest2', [1, 3]),   # match(1)bot1 vs bot2, match(3)bot2 vs bot3
        ('UsuarioTest3', [2, 3]),   # match(2)bot1 vs bot3, match(3)bot2 vs bot3
    ])
    def test_should_return_the_matches_played_by_a_user_requested(
        self,
        user_name,
        matches_expected,
    ):
        user = User.objects.filter(username=user_name).first()
        matches = list(get_matches_of_connected_user(user).values_list('id', flat=True))
        self.assertEqual(
            matches,
            matches_expected,
        )

    def test_should_format_matches_result_when_user1_do_GET_into_match_history(
        self,
    ):
        """
        Test for user1 who played matches 1 and 2
        match(1)bot1 vs bot2, match(2)bot1 vs bot3
        """
        matches = Match.objects.filter(id__in=[1, 2])
        self.assertEqual(
            get_matches_results(matches),
            [
                {
                    'match': matches[0],
                    'players': [
                        {'name': self.bot2.name, 'score': 2222, 'match_result': 2},
                        {'name': self.bot1.name, 'score': 1111, 'match_result': 0},
                    ]
                },
                {
                    'match': matches[1],
                    'players': [
                        {'name': self.bot3.name, 'score': 3333, 'match_result': 2},
                        {'name': self.bot1.name, 'score': 1111, 'match_result': 0},
                    ]
                },
            ],
        )
