from django.contrib.auth import get_user_model
from django.test import TestCase

from auth_app.models import Bot


class TestDeleteBot(TestCase):
    def test_should_return_302_when_user_makes_a_request(
        self,
    ):
        user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@email.com",
            password="my_pass",
        )
        self.client.force_login(user)
        Bot.objects.create(
            name='test_bot1',
            user=user,
        )
        response = self.client.post('/bots/1/delete')
        self.assertEqual(
            response.status_code,
            302,
        )
        self.assertEqual(
            response.url,
            '/mybots',
        )

    def test_should_delete_the_selected_bot_when_a_user_press_delete(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@email.com",
            password="my_pass",
        )
        self.client.force_login(user)
        bot = Bot.objects.create(
            name='test_bot1',
            user=user,
        )
        self.assertEqual(
            len(Bot.objects.filter(id=user.id)),
            1,
        )
        response = self.client.post('/bots/{bot_id}/delete'.format(bot_id=bot.id))
        messages = [str(msg) for msg in response.wsgi_request._messages]
        self.assertIn('Bot successfully removed', messages)
        with self.assertRaises(Bot.DoesNotExist):
            Bot.objects.get(pk=bot.id)

    def test_should_not_allow_delete_official_bot(self):
        user = get_user_model().objects.create_user(
            username="test_official_bot",
            email="test_official_bot@email.com",
            password="my_pass",
        )
        self.client.force_login(user)
        bot = Bot.objects.create(
            name='test_official_bot@email.com',
            user=user,
        )
        response = self.client.post('/bots/{bot_id}/delete'.format(bot_id=bot.id))
        messages = [str(msg) for msg in response.wsgi_request._messages]
        self.assertIn('The official bot cannot be removed', messages)
        Bot.objects.get(pk=bot.id)

    def test_should_raise_error_when_delete_if_bot_not_exists(self):
        user = get_user_model().objects.create_user(
            username="test_bot_not_exists",
            email="test_bot_not_exists@email.com",
            password="my_pass",
        )
        self.client.force_login(user)
        response = self.client.post('/bots/99/delete')
        messages = [str(msg) for msg in response.wsgi_request._messages]
        self.assertIn('The bot does not exists', messages)
