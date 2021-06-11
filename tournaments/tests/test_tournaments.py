from ..models import Tournament
from ..views import (
    CreateTournamentView,
    get_tournament_results,
    sort_position_table,
    TournamentResultsView,
)
from ..forms import TournamentForm
from auth_app.models import (
    Bot,
    User,
)
from development.views_api import save_match
from django.test import (
    RequestFactory,
    TestCase,
)
from django.http import HttpResponse
from unittest.mock import patch
from parameterized import parameterized


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
            tournament_results[0],
            {
                'bot': bot1.name,
                'total_match': 20,
                'total_match_won': 20,
                'total_score': 11100,
            }
        )
        self.assertEqual(
            tournament_results[1],
            {
                'bot': bot2.name,
                'total_match': 20,
                'total_match_won': 10,
                'total_score': 7100,
            }
        )
        self.assertEqual(
            tournament_results[2],
            {
                'bot': bot3.name,
                'total_match': 20,
                'total_match_won': 0,
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

    def test_sort_position_table_for_match_won_and_total_score(self):
        table = [
            {'bot': 'adminPro', 'total_match': 3, 'total_match_won': 0, 'total_score': -300},
            {'bot': 'brz', 'total_match': 3, 'total_match_won': 1, 'total_score': -300},
            {'bot': 'brzPro', 'total_match': 3, 'total_match_won': 2, 'total_score': -260},
            {'bot': 'admin', 'total_match': 3, 'total_match_won': 3, 'total_score': -300},
            {'bot': 'toxic', 'total_match': 3, 'total_match_won': 3, 'total_score': 400},
        ]
        self.assertEqual(
            sort_position_table(table),
            [
                {'bot': 'toxic', 'total_match': 3, 'total_match_won': 3, 'total_score': 400},
                {'bot': 'admin', 'total_match': 3, 'total_match_won': 3, 'total_score': -300},
                {'bot': 'brzPro', 'total_match': 3, 'total_match_won': 2, 'total_score': -260},
                {'bot': 'brz', 'total_match': 3, 'total_match_won': 1, 'total_score': -300},
                {'bot': 'adminPro', 'total_match': 3, 'total_match_won': 0, 'total_score': -300},
            ]
        )
