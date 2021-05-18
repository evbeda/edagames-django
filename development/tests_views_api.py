import json
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from .views_api import match_list
from parameterized import parameterized
from .views_api import convert_data
from unittest.mock import patch
from auth_app.models import User
from auth_app.models import Bot


class Tests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=False)
        self.user1 = User.objects.create(email='test1@gmail.com', username='UsuarioTest1')
        self.bot1 = Bot.objects.create(name='bot1', user=self.user1)
        self.user2 = User.objects.create(email='test2@gmail.com', username='UsuarioTest2')
        self.bot2 = Bot.objects.create(name='bot2', user=self.user2)

    @patch('development.views_api.convert_data')
    def test_match_list_ok(self, mock):
        status = 201
        return_mock = {
            'game_id': '1111',
            'bot_1': self.bot1.id,
            'score_p_1': 2000,
            'user_1': self.user1.id,
            'bot_2': self.bot2.id,
            'score_p_2': 1000,
            'user_2': self.user2.id
        }
        mock.return_value = return_mock
        request = self.factory.post('match/', json.dumps({}), content_type='application/json')
        responde = match_list(request)
        r = responde.status_code
        self.assertEqual(status, r)

    @patch('development.views_api.convert_data')
    def test_match_list_wrong(self, mock):
        status = 400
        mock.side_effect = KeyError
        request = self.factory.post('match/', json.dumps({}), content_type='application/json')
        responde = match_list(request)
        r = responde.status_code
        self.assertEqual(status, r)

    @parameterized.expand([
         [{'game_id': '1111', 'data': [('bot1', 2000), ('bot2', 1000)]}],
    ])
    def test_convert_data_ok(self, data):
        dic1 = {
            'game_id': '1111',
            'bot_1': self.bot1.id,
            'score_p_1': 2000,
            'user_1': self.user1.id,
            'bot_2': self.bot2.id,
            'score_p_2': 1000,
            'user_2': self.user2.id
        }
        dic2 = convert_data(data)

        self.assertEqual(dic1, dic2)

    @parameterized.expand([
         [{'game_id': '1111', 'date': [('bot1', 2000), ('bot2', 1000)]}],
    ])
    def test_convert_data_wrong(self, data):
        with self.assertRaises(KeyError):
            convert_data(data)
