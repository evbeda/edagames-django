from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .forms import UserRegisterForm
from parameterized import parameterized


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
        self.client.get('/')
        self.mock_messages.called_once()


class TestRegisterForm(TestCase):

    @parameterized.expand([
        (
            {
            'username': 'Eda',
            'email': 'edagames@evenbrite.com',
            'password1': 'AdGjLqEtUo',
            'password2': 'AdGjLqEtUo',
            },
            True,
        ),
        (
            {
            'username': 'Eda',
            'password1': 'AdGjLqEtUo',
            'password2': 'AdGjLqEtUo',
            },
            False,
        ),
    ])
    def test_new_register_form_is_valid(self, form_data, expected):
        form = UserRegisterForm(data=form_data)
        self.assertEqual(form.is_valid(), expected)
