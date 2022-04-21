from itertools import combinations

from parameterized import parameterized
from unittest.mock import patch

from django.test import (
    RequestFactory,
    TestCase,
)
from django.http import HttpResponse

from auth_app.models import (
    Bot,
    User,
)
from development.views_api import save_match
from development.models import Challenge
from tournaments.common.tournament_utils import (
    get_tournament_results,
    sort_position_table,
)
from tournaments.forms import TournamentForm
from tournaments.models import (
    Tournament,
    TournamentRegistration,
)
from tournaments.views import (
    CreateTournamentView,
    TournamentResultsView,
    RegistrationTournamentView,
)


class TestTournamentReistration(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='username1', password='password1', email='email1')
        self.tournament_registration = RegistrationTournamentView()

    def test_registration_get(self):
        request = self.factory.get('tournaments:tournament_registration')
        request.user = self.user
        response = RegistrationTournamentView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_registration_post(self):
        request = self.factory.post('tournaments:tournament_registration')
        request.user = self.user
        response = RegistrationTournamentView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(TournamentRegistration.objects.filter(user=self.user).exists())

    def test_unregistration_post(self):
        TournamentRegistration.objects.create(user=self.user)
        request = self.factory.post('tournaments:tournament_registration')
        request.user = self.user
        response = RegistrationTournamentView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TournamentRegistration.objects.filter(user=self.user).exists())


class TestTournament(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_superuser(username='username1', password='password1', email='email1')
        self.user1.is_staff = True
        self.tournament = CreateTournamentView()
        self.torneo2 = Tournament.objects.create(name='torneo2')

    def test_get_form_get(self):
        request = self.factory.get('tournaments:create_tournament')
        request.user = self.user1
        response = CreateTournamentView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_form_post(self):
        request = self.factory.post('tournaments:create_tournament')
        request.user = self.user1
        response = CreateTournamentView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ['torneo1', 200, True, True, True],
        ['torneo2', 000, False, False, False],
        ['torneo3', 422, True, True, False],
        ['torneo3', 500, True, True, False],
    ])
    @patch('tournaments.views.messages')
    @patch('requests.post')
    def test_form_valid(
        self,
        tourn_name,
        code,
        can_make_post,
        expected_tourn_not_exist,
        expected_post_response,
        post_patched,
        messages_patched,
    ):
        if can_make_post is True:
            post_patched.return_value = HttpResponse(status=code)
        tourn_before = Tournament.objects.filter(name=tourn_name).count()
        form = TournamentForm({'tournament': tourn_name, 'bots_selected': 'botito0,botito1', 'bots': '2'})
        form.fields['bots'].choices = [(0, 'botito0'), (1, 'botito1'), (2, 'botito2')]
        form.is_valid()
        view = CreateTournamentView()
        view.request = self.factory.post('tournaments:create_tournament')
        view.form_valid(form)
        if expected_tourn_not_exist is True:
            self.assertEqual(tourn_before, 0)
            tourn_after = Tournament.objects.filter(name=tourn_name).count()
            if expected_post_response is True:
                self.assertEqual(tourn_after, 1)
            else:
                self.assertEqual(tourn_after, 0)
        else:
            self.assertEqual(tourn_before, 1)

    def test_validation_data(self):
        form_data = {'tournament': '1', 'bots_selected': 'botito1,botito2', 'bots': ''}
        form = TournamentForm(data=form_data)
        form.is_valid()
        data = self.tournament.validation_data(form)
        self.assertEqual(data, ['1', 'botito1,botito2', ''])

    def test_tournament_results_view(self):
        tournament = Tournament.objects.create(name='test')
        user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        bot1 = Bot.objects.create(name='bot_1', user=user1)
        user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        bot2 = Bot.objects.create(name='bot_2', user=user2)
        user3 = User.objects.create(email='test3@gmail.com', username='UsuarioTest3')
        bot3 = Bot.objects.create(name='bot_3', user=user3)
        from itertools import combinations
        for bot_x, bot_y in combinations(
            [(bot1.name, 555), (bot2.name, 355), (bot3.name, 123)],
            2,
        ):
            match_info = {
                'game_id': '2222',
                'tournament_id': tournament.id,
                'data': [
                    [bot_x[0], bot_x[1]],
                    [bot_y[0], bot_y[1]],
                ]
            }
            for _ in range(10):
                save_match(match_info)
        tournament_results = get_tournament_results(tournament.id)
        self.assertEqual(
            tournament_results[bot1.name],
            {
                'total_match': 20,
                'total_match_won': 20,
                'total_match_tied': 0,
                'total_match_lost': 0,
                'total_score': 11100,
            }
        )
        self.assertEqual(
            tournament_results[bot2.name],
            {
                'total_match': 20,
                'total_match_won': 10,
                'total_match_tied': 0,
                'total_match_lost': 10,
                'total_score': 7100,
            }
        )
        self.assertEqual(
            tournament_results[bot3.name],
            {
                'total_match': 20,
                'total_match_won': 0,
                'total_match_tied': 0,
                'total_match_lost': 20,
                'total_score': 2460,
            }
        )

    def test_tournament_results_with_tie_values_view(self):
        tournament = Tournament.objects.create(name='test')
        user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        bot1 = Bot.objects.create(name='bot_1', user=user1)
        user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        bot2 = Bot.objects.create(name='bot_2', user=user2)
        user3 = User.objects.create(email='test3@gmail.com', username='UsuarioTest3')
        bot3 = Bot.objects.create(name='bot_3', user=user3)
        from itertools import combinations
        for bot_x, bot_y in combinations(
            [(bot1.name, 555), (bot2.name, 555), (bot3.name, 123)],
            2,
        ):
            match_info = {
                'game_id': '2222',
                'tournament_id': tournament.id,
                'data': [
                    [bot_x[0], bot_x[1]],
                    [bot_y[0], bot_y[1]],
                ]
            }
            for _ in range(10):
                save_match(match_info)
        tournament_results = get_tournament_results(tournament.id)
        self.assertEqual(
            tournament_results[bot1.name],
            {
                'total_match': 20,
                'total_match_won': 10,
                'total_match_tied': 10,
                'total_match_lost': 0,
                'total_score': 11100,
            }
        )
        self.assertEqual(
            tournament_results[bot2.name],
            {
                'total_match': 20,
                'total_match_won': 10,
                'total_match_tied': 10,
                'total_match_lost': 0,
                'total_score': 11100,
            }
        )
        self.assertEqual(
            tournament_results[bot3.name],
            {
                'total_match': 20,
                'total_match_won': 0,
                'total_match_tied': 0,
                'total_match_lost': 20,
                'total_score': 2460,
            }
        )

    def test_tournament_results_should_return_200_when_is_called_by_a_GET(
        self,
    ):
        tournament = Tournament.objects.create(name='test')
        request = self.factory.get('tournaments:tournament_details', params={'pk': tournament.id})
        request.user = self.user1
        response = TournamentResultsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_simple_tournament_results_1v1(self):
        tournament = Tournament.objects.create(name='test')
        user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        bot1 = Bot.objects.create(name='bot_1', user=user1)
        user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        bot2 = Bot.objects.create(name='bot_2', user=user2)
        results = [
            [bot1.name, 1000, bot2.name, 200],
            [bot1.name, 1000, bot2.name, 100],
            [bot1.name, 300, bot2.name, 500],
            [bot1.name, 150, bot2.name, 150],
            [bot1.name, 100, bot2.name, 100],
            [bot1.name, 50, bot2.name, 5000],
        ]
        for bot_x_name, bot_x_score, bot_y_name, bot_y_score in results:
            match_info = {
                'game_id': '2222',
                'tournament_id': tournament.id,
                'data': [
                    [bot_x_name, bot_x_score],
                    [bot_y_name, bot_y_score],
                ]
            }
            save_match(match_info)
        tournament_results = get_tournament_results(tournament.id)
        self.assertEqual(
            tournament_results[bot1.name],
            {
                'total_match': 6,
                'total_match_won': 2,
                'total_match_tied': 2,
                'total_match_lost': 2,
                'total_score': 2600,
            }
        )
        self.assertEqual(
            tournament_results[bot2.name],
            {
                'total_match': 6,
                'total_match_won': 2,
                'total_match_tied': 2,
                'total_match_lost': 2,
                'total_score': 6050,
            }
        )

    def test_sort_table_position_for_tournaments_results(self):
        table = {
            'tigresa': {
                'total_match': 2,
                'total_match_won': 0,
                'total_match_tied': 0,
                'total_match_lost': 2,
                'total_score': 50
            },
            'awd': {
                'total_match': 2,
                'total_match_won': 2,
                'total_match_tied': 0,
                'total_match_lost': 0,
                'total_score': 1500
            },
            'botocito': {
                'total_match': 2,
                'total_match_won': 1,
                'total_match_tied': 0,
                'total_match_lost': 1,
                'total_score': 200
            },
        }
        table_results = sort_position_table(table)
        self.assertEqual(
            table_results,
            [
                ('awd', 2, 2, 0, 0, 1500),
                ('botocito', 2, 1, 0, 1, 200),
                ('tigresa', 2, 0, 0, 2, 50)
            ]
        )

    def test_sort_table_position_for_tournaments_results_winner_highest_score(self):
        table = {
            'tigresa': {
                'total_match': 2,
                'total_match_won': 0,
                'total_match_tied': 0,
                'total_match_lost': 2,
                'total_score': 50
            },
            'awd': {
                'total_match': 2,
                'total_match_won': 1,
                'total_match_tied': 1,
                'total_match_lost': 0,
                'total_score': 1450
            },
            'botocito': {
                'total_match': 2,
                'total_match_won': 1,
                'total_match_tied': 1,
                'total_match_lost': 0,
                'total_score': 1500
            },
        }
        table_results = sort_position_table(table)
        self.assertEqual(
            table_results,
            [
                ('botocito', 2, 1, 1, 0, 1500),
                ('awd', 2, 1, 1, 0, 1450),
                ('tigresa', 2, 0, 0, 2, 50)
            ]
        )


class TestTournamentGenerator(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='username1', password='password1', email='email1')
        self.user.is_staff = True
        self.client.force_login(self.user)
        # clean all registration before create set for test
        TournamentRegistration.objects.all().delete()
        for index in range(20):
            registered_user = User.objects.create_user(
                username='username#{}'.format(index),
                password='password1',
                email='email{}@gmail.com'.format(index),
            )
            Bot.objects.create(
                name=registered_user.email,
                user=registered_user,
            )
            TournamentRegistration.objects.create(user=registered_user)

    def test_generate_tournament_get(self):
        response = self.client.post('/tournament_generator')
        self.assertEqual(response.status_code, 301)

    def test_generate_tournament_already_exists(self):
        tournament_name = "Already Exists"
        Tournament.objects.create(name=tournament_name)
        response = self.client.post(
            '/tournament_generator/',
            {
                "tournament_name": tournament_name,
                "max_players": 12
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str([m for m in response.wsgi_request._messages][0]),
            (
                'It is not possible to create this record, a tournament'
                ' already exists with the name Already Exists. Try a new name'
            ),
        )

    def test_generate_tournament_successfully(self):
        tournament_name = "New Tournament"
        response = self.client.post(
            '/tournament_generator/',
            {
                "tournament_name": tournament_name,
                "max_players": 12
            },
        )
        self.assertEqual(response.status_code, 302)
        tournament_1 = Tournament.objects.get(name__contains='New Tournament #1')
        tournament_2 = Tournament.objects.get(name__contains='New Tournament #2')
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_1).count(),
            len(list(combinations(list(range(12)), 2))),
        )
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_2).count(),
            len(list(combinations(list(range(8)), 2))),
        )

    def test_generate_tournament_successfully_exact(self):
        tournament_name = "New Tournament"
        response = self.client.post(
            '/tournament_generator/',
            {
                "tournament_name": tournament_name,
                "max_players": 10
            },
        )
        self.assertEqual(response.status_code, 302)
        tournament_1 = Tournament.objects.get(name__contains='New Tournament #1')
        tournament_2 = Tournament.objects.get(name__contains='New Tournament #2')
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_1).count(),
            len(list(combinations(list(range(10)), 2))),
        )
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_2).count(),
            len(list(combinations(list(range(10)), 2))),
        )
