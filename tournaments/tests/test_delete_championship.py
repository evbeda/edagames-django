from tournaments.models import (
    Tournament,
    TournamentRegistration,
)

from django.test import (
    RequestFactory,
    TestCase,
)

from auth_app.models import (
    Bot,
    User,
)

from parameterized import parameterized


class TestDeleteChampionship(TestCase):

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

    @parameterized.expand([
        (
            "should_return_error_msg_when_delete_tournament_is_linked_by_final_tournament",
            "2",
            'Cant delete a tournament that is linked to a FINAL',
            3,
            "Tournament",
        ),
        (
            "test_should_delete_the_selected_final_tournament_when_a_user_press_delete",
            "1",
            'Championship and his tournaments successfully removed',
            0,
            "deletion Tournament",
        ),
    ])
    def test_delete_final_tournaments_in_diferent_cases(
        self,
        name,
        id,
        message_expected,
        final_tournament_instances,
        champ_name
    ):
        response = self.client.post(
            '/create_championship/',
            {
                "championship_name": champ_name,
                "max_players": 10,
                "finalist_users_per_tournament": 2,
            },
        )
        response = self.client.post(f'/tournaments/{id}/delete')
        messages = [str(msg) for msg in response.wsgi_request._messages]
        self.assertIn(message_expected, messages)
        self.assertEqual(len(Tournament.objects.all()), final_tournament_instances)
