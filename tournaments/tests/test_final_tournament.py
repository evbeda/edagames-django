from django.test import (
    RequestFactory,
    TestCase,
)
from unittest.mock import patch
from auth_app.models import Bot, User
from tournaments.common.tournament_utils import (
    create_registrations_and_challenges_for_final_tournament,
    get_finalist_users)
from tournaments.models import (
    Championship,
    FinalTournamentRegistration,
    Tournament,
    TournamentRegistration)
from tournaments.views import ChampionshipHistoryView, FinalistUserView


class TestFinalTournamentRegistrationModel(TestCase):

    def test_str(self):
        user = User.objects.create_user(username='username1', password='password1', email='email1@gmail.com')
        final_tournament = Tournament.objects.create(name="final-test-1")
        championship = Championship.objects.create(
            name="champ-test-1",
            tournament_bots=3,
            final_tournament=final_tournament)
        final_tournament.championship = championship
        tournament_registration = FinalTournamentRegistration.objects.create(user=user, championship=championship)
        self.assertEqual(
            str(tournament_registration),
            f'email1@gmail.com, champ-test-1 ({tournament_registration.id})'
        )


class TestFinalTournamentRegistration(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='username1', password='password1', email='email1')
        self.user.is_staff = True
        self.client.force_login(self.user)
        self.final_tournament_view = FinalistUserView()
        self.final_tournament = Tournament.objects.create(name="final-test-3")
        self.championship = Championship.objects.create(
            name="champ-test-3",
            tournament_bots=3,
            final_tournament=self.final_tournament)
        self.final_tournament.championship = self.championship
        self.tournament = Tournament.objects.create(name="test", championship=self.championship)
        # clean all registration before create set for test
        TournamentRegistration.objects.all().delete()
        FinalTournamentRegistration.objects.all().delete()
        for index in range(5):
            registered_user = User.objects.create_user(
                username=f'username#{index}',
                password='password1',
                email=f'email{index}@gmail.com',
            )
            Bot.objects.create(
                name=registered_user.email,
                user=registered_user,
            )
            TournamentRegistration.objects.create(user=registered_user)

    @patch('tournaments.common.tournament_utils.get_tournament_results', return_value={
        "email0@gmail.com": {
            "total_match": 380,
            "total_match_won": 0,
            "total_match_tied": 0,
            "total_match_lost": 2,
            "total_score": 10000,
        },
        "email1@gmail.com": {
            "total_match": 380,
            "total_match_won": 2,
            "total_match_tied": 1,
            "total_match_lost": 3,
            "total_score": 10001,
        },
        "email2@gmail.com": {
            "total_match": 380,
            "total_match_won": 4,
            "total_match_tied": 2,
            "total_match_lost": 4,
            "total_score": 10002,
        },
        "email3@gmail.com": {
            "total_match": 380,
            "total_match_won": 6,
            "total_match_tied": 3,
            "total_match_lost": 5,
            "total_score": 10003,
        },
        "email4@gmail.com": {
            "total_match": 380,
            "total_match_won": 8,
            "total_match_tied": 8,
            "total_match_lost": 6,
            "total_score": 10004,
        }})
    @patch('tournaments.common.tournament_utils.sort_position_table', return_value=[
        ("email4@gmail.com", 380, 8, 4, 6, 10004),
        ("email3@gmail.com", 380, 6, 3, 5, 10003),
        ("email2@gmail.com", 380, 4, 2, 4, 10002),
        ("email1@gmail.com", 380, 2, 1, 3, 10001),
        ("email0@gmail.com", 380, 0, 0, 10000),
    ])
    def test_get_finalist_users(self, patch_function1, patch_function2):
        result = get_finalist_users(self.championship, self.championship.tournament_bots)
        expected = [
            User.objects.get(email="email4@gmail.com"),
            User.objects.get(email="email3@gmail.com"),
            User.objects.get(email="email2@gmail.com")]
        self.assertEqual(result, expected)

    @patch('tournaments.common.tournament_utils.get_finalist_users')
    def test_create_registrations_and_challenges_for_final_tournament(self, patch_function):
        patch_function.return_value = [
            User.objects.get(email="email4@gmail.com"),
            User.objects.get(email="email3@gmail.com"),
            User.objects.get(email="email2@gmail.com")]
        create_registrations_and_challenges_for_final_tournament(
            self.championship,
            self.final_tournament,
            self.championship.tournament_bots)
        result = list(FinalTournamentRegistration.objects.all())
        expected = list(FinalTournamentRegistration.objects.filter(championship=self.championship.pk))
        self.assertEqual(result, expected)

    @patch('tournaments.common.tournament_utils.get_finalist_users')
    def test_create_registrations_and_challenges_for_final_tournament_existing_registration(self, patch_function):
        patch_function.return_value = [
            User.objects.get(email="email4@gmail.com"),
            User.objects.get(email="email3@gmail.com"),
            User.objects.get(email="email2@gmail.com")]
        user_registrated = User.objects.get(email="email4@gmail.com")
        FinalTournamentRegistration.objects.create(user=user_registrated, championship=self.championship)
        create_registrations_and_challenges_for_final_tournament(
            self.championship,
            self.final_tournament,
            self.championship.tournament_bots)
        result = list(FinalTournamentRegistration.objects.all())
        expected = list(FinalTournamentRegistration.objects.filter(championship=self.championship.pk))
        self.assertEqual(result, expected)


class TestChampionshipHistoryView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='username1', password='password1', email='email1')
        self.user.is_staff = True
        self.client.force_login(self.user)
        self.view = ChampionshipHistoryView()
        self.final_tournament = Tournament.objects.create(name="final-test-3")
        self.championship = Championship.objects.create(
            name="champ-test-3",
            tournament_bots=3,
            final_tournament=self.final_tournament)
        self.final_tournament.championship = self.championship
        self.tournament = Tournament.objects.create(name="test", championship=self.championship)
        # clean all registration before create set for test
        TournamentRegistration.objects.all().delete()
        FinalTournamentRegistration.objects.all().delete()
        for index in range(5):
            registered_user = User.objects.create_user(
                username=f'username#{index}',
                password='password1',
                email=f'email{index}@gmail.com',
            )
            Bot.objects.create(
                name=registered_user.email,
                user=registered_user,
            )
            TournamentRegistration.objects.create(user=registered_user)

    def test_get_queryset(self):
        result = list(self.view.get_queryset())
        expected = list(Championship.objects.all())
        self.assertEqual(result, expected)

    def test_get(self):
        request = self.factory.get('tournaments:championship_list')
        request.user = self.user
        response = ChampionshipHistoryView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestFinalistUserView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='username1', password='password1', email='email1')
        self.user.is_staff = True
        self.client.force_login(self.user)
        self.view = FinalistUserView()
        self.final_tournament = Tournament.objects.create(name="final-test-3")
        self.championship = Championship.objects.create(
            name="champ-test-3",
            tournament_bots=3,
            final_tournament=self.final_tournament)
        self.final_tournament.championship = self.championship
        self.tournament = Tournament.objects.create(name="test", championship=self.championship)
        # clean all registration before create set for test
        TournamentRegistration.objects.all().delete()
        FinalTournamentRegistration.objects.all().delete()
        for index in range(5):
            registered_user = User.objects.create_user(
                username=f'username#{index}',
                password='password1',
                email=f'email{index}@gmail.com',
            )
            Bot.objects.create(
                name=registered_user.email,
                user=registered_user,
            )
            TournamentRegistration.objects.create(user=registered_user)

    def test_get_queryset(self):
        request = self.factory.get('tournaments:finalist_users', {'pk': self.championship.pk})
        request.user = self.user
        response = FinalistUserView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_create_registration(self):
        response = self.client.post(f'/create_registration/{self.championship.pk}')
        self.assertEqual(response.status_code, 302)
