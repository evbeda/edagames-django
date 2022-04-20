from django.test import TestCase
from django.contrib.auth import get_user_model


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
