from ..models import Tournament
from ..views import CreateTournamentView
from ..forms import TournamentForm
from auth_app.models import User
from django.test import (
    RequestFactory,
    TestCase,
)
from unittest.mock import patch
from parameterized import parameterized


class TestCreateTournamentView(TestCase):
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
        ['torneo1', True],
        ['torneo2', False],
    ])
    @patch('tournaments.views.messages')
    def test_form_valid(self, tourn_name, expected, messages_patched):
        tour_test = Tournament.objects.filter(name=tourn_name).count()
        form = TournamentForm({'tournament': tourn_name, 'bots_selected': ['botito0', 'botito1'], 'bots': '2'})
        form.fields['bots'].choices = [(0, 'botito0'), (1, 'botito1'), (2, 'botito2')]
        form.is_valid()
        view = CreateTournamentView()
        view.request = self.factory.post('tournaments:create_tournament')
        view.form_valid(form)
        if expected is True:
            self.assertEqual(tour_test, 0)
        else:
            self.assertEqual(tour_test, 1)

    def test_validation_data(self):
        form_data = {'tournament': '1', 'bots_selected': '1', 'bots': ''}
        form = TournamentForm(data=form_data)
        form.is_valid()
        data = self.tournament.validation_data(form)
        self.assertEqual(data, ['1', '1', ''])
