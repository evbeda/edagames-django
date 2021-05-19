from auth_app.models import User
from django.test import RequestFactory, TestCase, Client
from ..views import ChallengeView
from django.urls import reverse_lazy
# import json
import requests
# from parameterized import parameterized


class TestChallengeView(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_get_form_get(self):
        request = self.factory.get('development:challenge')
        request.user = self.user
        response = ChallengeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

# class TestChallengeView(TestCase):
#     def setUp(self):
#         self.client = Client()
    
#     def test_get_form_get(self):
#         response = self.client.get(reverse_lazy('development:challenge'))
#         self.assertEqual(response.status_code, 200)
