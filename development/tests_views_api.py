from rest_framework.test import APIRequestFactory
from django.test import TestCase
from .views_api import match_list


# factory = APIRequestFactory()
factory = APIRequestFactory(enforce_csrf_checks=True)
# request = factory.post('/notes/', {'title': 'new idea'})
request = factory.post('/match/', json.dumps("bot_one": "Andres", "bot_two": "Valentina", "score_p_one": 4, "score_p_two": 6, "board_id":"111111"}), content_type='application/json')

serializer.data = {"bot_one": "Andres", "bot_two": "Valentina", "score_p_one": 4, "score_p_two": 6, "board_id":"111111"}
status=201

class Tests(TestCase):
    def test_match_list(self, request, serializer.data):
        responde = match_list(request)
        self.assertEqual(JsonResponse(serializer.data, status=201), responde)
