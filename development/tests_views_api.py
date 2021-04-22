import json
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from .views_api import match_list
from parameterized import parameterized


class Tests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=False)

    @parameterized.expand([
        [{"bot_one": "Andres", "bot_two": "Valentina", "score_p_one": 4, "score_p_two": 6, "board_id": "111111"}, 201],
        [{"bot_uno": "Andres", "bot_two": "Valentina", "score_p_one": 4, "score_p_two": 6, "board_id": "111111"}, 400],
    ])
    def test_match_list(self, d, s):
        request = self.factory.post('match/', json.dumps(d), content_type='application/json')
        responde = match_list(request)
        r = responde.status_code
        self.assertEqual(s, r)
