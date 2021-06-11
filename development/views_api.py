from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from development.serializer import (
    MatchSerializer,
)
from auth_app.models import Bot
from development.models import (
    Match,
    MatchMembers,
)
from django.db import transaction


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
        key error from convert_data_for_match when tray to generate new dict
    """
    if request.method == 'POST':
        dic_data = JSONParser().parse(request)
        serializer_match = MatchSerializer(data=dic_data)
        if serializer_match.is_valid():
            save_match(serializer_match.validated_data)
            return JsonResponse(
                serializer_match.data,
                status=201,
            )
        else:
            return JsonResponse(
                {'Error': 'The Server has created a wrong data key'},
                status=400,
            )


@transaction.atomic
def save_match(match_info):
    match = Match.objects.create(
        game_id=match_info['game_id'],
        tournament_id=match_info['tournament_id'],
    )
    match_info['data'].sort(key=lambda x: x[1], reverse=True)
    match_members = [
        MatchMembers(
            bot=Bot.objects.get(name=name),
            score=score,
            match=match,
            winner=(match_info['data'][0][0] == name),
        )
        for name, score in match_info['data']
    ]
    MatchMembers.objects.bulk_create(match_members)
