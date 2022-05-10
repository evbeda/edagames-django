from django.contrib.auth import get_user_model
from django.test import TestCase

from tournaments.models import Tournament


class TestDeleteBot(TestCase):
    def test_user_should_be_redirected_when_delete_tournament(
        self,
    ):
        user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@email.com",
            password="my_pass",
        )
        self.client.force_login(user)
        Tournament.objects.create(
            name='tournament_test',
        )
        response = self.client.post('/tournaments/1/delete')
        self.assertEqual(
            response.status_code,
            302,
        )
        self.assertEqual(
            response.url,
            '/tournaments_pending/',
        )

    def test_should_delete_the_selected_tournament_when_a_user_press_delete(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@email.com",
            password="my_pass",
        )
        self.client.force_login(user)
        tournament = Tournament.objects.create(
            name='tournament_test',
        )
        self.assertEqual(
            len(Tournament.objects.filter(id=user.id)),
            1,
        )
        response = self.client.post(
            '/tournaments/{tournament_id}/delete'.format(
                tournament_id=tournament.id
            )
        )
        messages = [str(msg) for msg in response.wsgi_request._messages]
        self.assertIn('Tournament successfully removed', messages)
        with self.assertRaises(Tournament.DoesNotExist):
            Tournament.objects.get(pk=tournament.id)

    def test_should_return_error_msg_when_delete_tournament_if_bot_doesnot_exists(self):
        user = get_user_model().objects.create_user(
            username="test_bot_not_exists",
            email="test_bot_not_exists@email.com",
            password="my_pass",
        )
        self.client.force_login(user)
        response = self.client.post('/tournaments/99/delete')
        messages = [str(msg) for msg in response.wsgi_request._messages]
        self.assertIn('The tournament does not exists', messages)
