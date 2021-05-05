from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from development.serializer import MatchSerializer


@csrf_exempt
def match_list(request):
    if request.method == 'POST':
        req_data = JSONParser().parse(request)
        data = {}
        data['game_id'] = req_data["game_id"]
        for i, name, score in enumerate(req_data["data"], 1):
            data[f'bot_{i}'] = name
            data[f'score_p_{i}'] = score
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
