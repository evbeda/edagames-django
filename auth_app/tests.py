from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.contrib.messages import get_messages


class TestViewsAnonimous(TestCase):
    def test_home_no_authenticated(self):
        response = self.client.get('')
        self.assertEqual(
            response.status_code,
            302,
        )
        self.assertEqual(
            response.url,
            '/login/?next=/',
        )
        self.assertRedirects(
            response,
            '/login/?next=/',
        )


class TestViewsAuthenticated(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            "test_user",
            "test_user@email.com",
            "my_pass",
        )
        self.mock_messages = patch(
            'auth_app.signals.messages',
            return_value='andando').start()
        self.client.force_login(self.user)

    def test_home_authenticated_no_tasks(self):
        response = self.client.get('/')

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_token_message(self):
        response = self.client.get('/')
        message = get_messages(response)
        print(message)
        self.mock_messages.called_once()
