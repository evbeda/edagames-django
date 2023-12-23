from django.test import TestCase
from django.contrib.auth import get_user_model
from auth_app.forms import UserRegisterForm
from parameterized import parameterized
from unittest.mock import patch

from auth_app.pipeline import create_bot
from auth_app.models import (
    Bot,
    User,
    UserManager,
)
from tournaments.models import TournamentRegistration


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
        self.client.force_login(self.user)

    def test_home_authenticated_no_tasks(self):
        response = self.client.get('/')

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_registration(self):
        self.assertEqual(len(get_user_model().objects.all()), 1)
        data = {
            'username': 'CC',
            'email': 'cc@email.com',
            'password1': 'AdGjLqEtUo',
            'password2': 'AdGjLqEtUo',
        }
        response = self.client.post('/register/', data)
        self.assertEqual(
            response.status_code,
            302,
        )
        self.assertEqual(len(get_user_model().objects.all()), 2)
        self.assertEqual(get_user_model().objects.last().username, 'CC')


class TestRegisterForm(TestCase):

    @parameterized.expand([
        (
            {
                'username': 'CC',
                'email': 'cc@email.com',
                'password1': 'AdGjLqEtUo',
                'password2': 'AdGjLqEtUo',
            },
            True,
        ),
        (
            {
                'username': 'CC',
                'password1': 'AdGjLqEtUo',
                'password2': 'AdGjLqEtUo',
            },
            False,
        ),
    ])
    def test_new_register_form_is_valid(self, form_data, expected):
        form = UserRegisterForm(data=form_data)
        self.assertEqual(form.is_valid(), expected)


class TestUserManager(TestCase):

    def setUp(self):
        self.user_manager = UserManager()

    def test_create_superuser(self):
        super_user = get_user_model().objects.create_superuser(
            'admin@eventbrite.com',
            'admin',
            '1234',
        )

        self.assertTrue(isinstance(super_user, User))
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)

    @patch.object(UserManager, 'create_user')
    @patch.object(Bot.objects, 'create')
    @patch.object(TournamentRegistration.objects, 'create')
    def test_mock_create_superuser(self, mock_create_tournament_registration, mock_create_bot, mock_create_user):
        email = 'admin@eventbrite.com'
        name = 'admin'
        pw = '1234'
        get_user_model().objects.create_superuser(
            email,
            name,
            pw,
        )

        mock_create_user.is_called_once_with(
            email,
            name,
            pw,
        )
        mock_create_tournament_registration.is_called_once()
        mock_create_bot.is_called_once_with()


class TestUser(TestCase):

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            'normal@eventbrite.com',
            'normal',
            '1234',
        )

    def test_str_user(self):
        self.assertEqual(
            str(self.user),
            '@normal',
        )


class TestBot(TestCase):
    def test_create_bot_when_a_user_is_created(self):
        strategy = ''
        user = get_user_model().objects.create_user(
            'normal@eventbrite.com',
            'normal',
            '1234',
        )
        response = ''
        return_value = create_bot(strategy, user, response)
        self.assertTrue(Bot.objects.filter(user=user,).exists())
        expected_value = {
            'is_new': False,
            'user': user,
        }
        self.assertEqual(
            return_value,
            expected_value
        )
