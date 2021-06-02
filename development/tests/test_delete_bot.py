from django.test import TestCase
from django.contrib.auth import get_user_model
from auth_app.models import Bot


class TestDeleteBot(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test_user",
            "test_user@email.com",
            "my_pass",
        )
        self.client.force_login(self.user)

    def test_should_return_302_when_user_makes_a_request(
        self,
    ):
        Bot.objects.create(
            name='test_bot1',
            user=self.user,
        )
        response = self.client.get('/bots/1/delete')
        self.assertEqual(
            response.status_code,
            302,
        )
        self.assertEqual(
            response.url,
            '/mybots',
        )

    def test_should_delete_the_selected_bot_when_a_user_press_delete(self):
        Bot.objects.create(
            name='test_bot1',
            user=self.user,
        )
        self.assertEqual(
            len(Bot.objects.filter(id=self.user.id)),
            1,
        )
        self.client.get('/bots/1/delete')
        self.assertEqual(
            len(Bot.objects.filter(id=self.user.id)),
            0,
        )
