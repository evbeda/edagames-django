import json
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from .views_api import match_list
from parameterized import parameterized
from .views_api import convert_data
from unittest.mock import patch


class Tests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=False)

    @parameterized.expand([
        [{'game_id': '1111', 'bot_1': 'pablo', 'score_p_1': 2000, 'bot_2': 'pedro', 'score_p_2': 1000},
         201],
        [None, 400],
    ])
    @patch('development.views_api.convert_data')
    def test_match_list(self, return_mock, status, mock):
        if return_mock is not None:
            mock.return_value = return_mock
        else:
            mock.side_effect = KeyError
        request = self.factory.post('match/', json.dumps({}), content_type='application/json')
        responde = match_list(request)
        r = responde.status_code
        self.assertEqual(status, r)

    @parameterized.expand([
        [{'game_id': '1111', 'data': [('pablo', 2000), ('pedro', 1000)]},
         {'game_id': '1111', 'bot_1': 'pablo', 'score_p_1': 2000, 'bot_2': 'pedro', 'score_p_2': 1000},
         True],
        [{'game_id': '1111', 'date': [('pablo', 2000), ('pedro', 1000)]},
         None,
         False],
    ])
    def test_convert_data(self, data, expected, flag):
        if flag:
            self.assertEqual(convert_data(data), expected)
        else:
            with self.assertRaises(KeyError):
                convert_data(data)
