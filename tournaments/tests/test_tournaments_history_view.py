from itertools import combinations
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from edagames.settings import (
    SERVER_PORT,
    SERVER_URL,
)
from auth_app.models import (
    Bot,
    User,
)
from development.models import Challenge
from tournaments.models import Tournament


class TestTournamentsHistoryView(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create_user(
            "test_user1",
            "test_user1@email.com",
            "my_pass",
        )
        self.client.force_login(self.user1)

    def test_should_return_200_when_user1_makes_a_request_for_tournaments_history(
        self,
    ):
        response = self.client.get('/tournaments_history/')
        self.assertEqual(
            response.status_code,
            200,
        )

    def test_should_use_tournament_history_template_when_user_makes_a_request(self):
        response = self.client.get('/tournaments_history/')
        self.assertTemplateUsed(
            response,
            'tournaments/tournaments_history.html',
        )


class TestPendingTournamentsView(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create_user(
            "test_user1",
            "test_user1@email.com",
            "my_pass",
        )
        self.client.force_login(self.user1)

    def test_should_return_200_when_user1_makes_a_request_for_tournaments_pending(
        self,
    ):
        response = self.client.get('/tournaments_pending/')
        self.assertEqual(
            response.status_code,
            200,
        )

    def test_should_return_200_when_user1_makes_a_request_for_tournaments_pending_submit(
        self,
    ):
        pending_tournament = Tournament.objects.create(status=Tournament.TOURNAMENT_PENDING_STATUS)
        bots = []
        for index in range(3):
            registered_user = User.objects.create_user(
                username='username#{}'.format(index),
                password='password1',
                email='email{}@gmail2.com'.format(index),
            )
            bots.append(
                Bot.objects.create(
                    name=registered_user.email,
                    user=registered_user,
                )
            )

        challenges = combinations(bots, 2)
        for bot_challenger, bots_challenged in challenges:
            challenge = Challenge.objects.create(
                bot_challenger=bot_challenger,
                tournament=pending_tournament,
            )
            challenge.bots_challenged.add(bots_challenged)
        with patch(
            'requests.post',
        ) as server_request_get_mocked:
            response = self.client.post('/tournaments_pending/?tournament={}'.format(pending_tournament.id))
            self.assertEqual(server_request_get_mocked.call_count, 3)
            self.assertEqual(
                server_request_get_mocked.call_args_list[0][0][0],
                f'{SERVER_URL}:{SERVER_PORT}/tournament'
            )
            self.assertEqual(
                server_request_get_mocked.call_args_list[1][0][0],
                f'{SERVER_URL}:{SERVER_PORT}/tournament'
            )
            self.assertEqual(
                server_request_get_mocked.call_args_list[2][0][0],
                f'{SERVER_URL}:{SERVER_PORT}/tournament'
            )
            self.assertEqual(
                server_request_get_mocked.call_args_list[0][1]['json'],
                {
                    'tournament_id': str(pending_tournament.id),
                    'challenges': [('email0@gmail2.com', 'email1@gmail2.com')]
                }
            )
            self.assertEqual(
                server_request_get_mocked.call_args_list[1][1]['json'],
                {
                    'tournament_id': str(pending_tournament.id),
                    'challenges': [('email0@gmail2.com', 'email2@gmail2.com')]
                }
            )
            self.assertEqual(
                server_request_get_mocked.call_args_list[2][1]['json'],
                {
                    'tournament_id': str(pending_tournament.id),
                    'challenges': [('email1@gmail2.com', 'email2@gmail2.com')]
                }
            )
        self.assertEqual(
            response.status_code,
            200,
        )
