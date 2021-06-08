from django.test import TestCase
from django.contrib.auth import get_user_model


class TestFAQView(TestCase):

    def setUp(self):
        super().setUp()
        self.user1 = get_user_model().objects.create_user(
            "test_user1",
            "test_user1@email.com",
            "my_pass",
        )
        self.client.force_login(self.user1)

    def test_should_return_200_when_user_makes_a_request_for_FAQ(self):
        response = self.client.get('/faq/')
        self.assertEqual(
            response.status_code,
            200,
        )
