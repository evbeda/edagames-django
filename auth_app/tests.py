from django.test import TestCase
from django.contrib.auth import get_user_model
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
            'username': 'Eda',
            'email': 'edagames@evenbrite.com',
            'password1': 'AdGjLqEtUo',
            'password2': 'AdGjLqEtUo',
        }
        response = self.client.post('/register/', data)
        self.assertEqual(
            response.status_code,
            302,
        )
        self.assertEqual(len(get_user_model().objects.all()), 2)
        self.assertEqual(get_user_model().objects.last().username, 'Eda')
        self.assertTrue(get_user_model().objects.last().token)


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
        print('primero')