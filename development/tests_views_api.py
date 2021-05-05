import json
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from .views_api import match_list
from parameterized import parameterized


class Tests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=False)

    @parameterized.expand([
        [{"game_id": "1111", "data": [('pablo', 2000), ('pedro', 1000)]}, 201],
        [{"game_id": "1111", "data": [('pablo', 2000), ('pedro', 1000)]}, 400],
    ])
    def test_match_list(self, d, s):
        request = self.factory.post('match/', json.dumps(d), content_type='application/json')
        responde = match_list(request)
        r = responde.status_code
        self.assertEqual(s, r)
