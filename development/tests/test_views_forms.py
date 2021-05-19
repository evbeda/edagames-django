from auth_app.models import User
from django.test import RequestFactory, TestCase
from ..views import ChallengeView


class TestChallengeView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_get_form_get(self):
        request = self.factory.get('development:challenge')
        request.user = self.user
        response = ChallengeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_form_post(self):
        request = self.factory.post('development:challenge')
        request.user = self.user
        response = ChallengeView.as_view()(request)
        self.assertEqual(response.status_code, 200)


# def test_form_valid(self):
#     request = self.factory.post('https://localhost:5000/challenge', self.data)
#     request.user = self.user
#     response = ChallengeView.as_view()(request)
#     self.assertEqual(response.status_code, 200)
