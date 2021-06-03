from ..models import Tournament
from edagames.settings import (
    SERVER_PORT,
    SERVER_URL,
)
from django.test import TestCase
from unittest.mock import patch
from tournaments.server_requests import generate_combination
import json
from unittest.mock import MagicMock


class TestServerRequests(TestCase):

    def test_generate_combination(self):
        tourn_name = 'Torneo 1'
        bots_chosen = 'bot1,bot2,bot3'
        Tournament.objects.create(name=tourn_name)
        mocked_response = MagicMock(json=lambda x: json.loads(x), spec=["json"])
        with patch(
            'requests.post',
            return_value=mocked_response,
        ) as request_get_mocked:
            generate_combination(
                tourn_name,
                bots_chosen,
            )
            request_get_mocked.assert_called_once_with(
                f'{SERVER_URL}:{SERVER_PORT}/tournament',
                json={
                    'tournament_id': str(Tournament.objects.only('id').get(name=tourn_name).id),
                    'challenges': [
                        ('bot1', 'bot2'),
                        ('bot1', 'bot3'),
                        ('bot2', 'bot3')
                    ]
                }
            )
