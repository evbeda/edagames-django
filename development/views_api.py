from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from development.serializer import MatchSerializer
from auth_app.models import Bot


@csrf_exempt
def match_list(request):
    """
    Recieve data from server and validate data for Math class

    Parameters
    -------
    json
        request
    Returns
    -------
    json
        response to server that contains a dic and a status
    Raises
    -------
    KeyError
        key error from convert_data when tray to generate new dict
    """
    if request.method == 'POST':
        dic_data = JSONParser().parse(request)
        try:
            data = convert_data(dic_data)
        except KeyError as e:
            return JsonResponse({'error': str(e)}, status=400)
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)


def convert_data(req_data):
    """ Recieve a dictionary and return a new dictionary. """
    data = {}
    data['game_id'] = req_data["game_id"]
    data['tournament_id'] = req_data['tournament_id']
    for i, (name, score) in enumerate(req_data["data"], 1):
        bot = Bot.objects.filter(name=name)[0]
        data[f'bot_{i}'] = bot.id
        data[f'score_p_{i}'] = score
        data[f'user_{i}'] = bot.user.id
    return data
