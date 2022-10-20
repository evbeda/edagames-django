# from django.contrib.auth import get_user_model
from itertools import combinations

from django.test import (
    RequestFactory,
    TestCase,
)

from development.models import Challenge

from tournaments.models import (
    Championship,
    Tournament,
    TournamentRegistration,
)


from auth_app.models import (
    Bot,
    User,
)


class TestChampionshipGenerator(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='username1', password='password1', email='email1')
        self.user.is_staff = True
        self.client.force_login(self.user)
        # clean all registration before create set for test
        TournamentRegistration.objects.all().delete()
        for index in range(20):
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

    def test_generate_generate_get(self):
        response = self.client.post('/create_championship')
        self.assertEqual(response.status_code, 301)

    def test_generate_championship_already_exists(self):
        championship_name = "Already Exists"
        Championship.objects.create(
            name=championship_name,
            tournament_bots=10,
            final_tournament=Tournament.objects.create(name="final_tournament"),
        )
        response = self.client.post(
            '/create_championship/',
            {
                "championship_name": championship_name,
                "max_players": 10,
                "finalist_users_per_tournament": 2,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            str([m for m in response.wsgi_request._messages][0]),
            (
                'It is not possible to create this record, a championship'
                ' already exists with the name Already Exists. Try a new name'
            ),
        )

    def test_generate_championship_successfully(self):
        championship_name = "New Tournament"
        response = self.client.post(
            '/create_championship/',
            {
                "championship_name": championship_name,
                "max_players": 12,
                "finalist_users_per_tournament": 2,

            },
        )
        self.assertEqual(response.status_code, 302)
        tournament_1 = Tournament.objects.get(name__contains='New Tournament #1')
        tournament_2 = Tournament.objects.get(name__contains='New Tournament #2')
        tournament_final = Tournament.objects.get(name__contains='New Tournament FINAL')
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_1).count(),
            len(list(combinations(list(range(12)), 2))),
        )
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_2).count(),
            len(list(combinations(list(range(8)), 2))),
        )
        # the final tournament creates in a first instance as an empty tournament
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_final).count(),
            len(list(combinations(list(range(0)), 1))),
        )

    def test_generate_championship_successfully_exact(self):
        championship_name = "Other Tournament"
        response = self.client.post(
            '/create_championship/',
            {
                "championship_name": championship_name,
                "max_players": 10,
                "finalist_users_per_tournament": 2,
            },
        )
        self.assertEqual(response.status_code, 302)
        tournament_1 = Tournament.objects.get(name__contains='Other Tournament #1')
        tournament_2 = Tournament.objects.get(name__contains='Other Tournament #2')
        tournament_final = Tournament.objects.get(name__contains='Other Tournament FINAL')
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_1).count(),
            len(list(combinations(list(range(10)), 2))),
        )
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_2).count(),
            len(list(combinations(list(range(10)), 2))),
        )
        # the final tournament creates in a first instance as an empty tournament
        self.assertEqual(
            Challenge.objects.filter(tournament=tournament_final).count(),
            len(list(combinations(list(range(0)), 1))),
        )
