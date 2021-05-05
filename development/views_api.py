from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from development.serializer import MatchSerializer


@csrf_exempt
def match_list(request):
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


def convert_data(self, req_data):
    data = {}
    data['game_id'] = req_data["game_id"]
    for i, (name, score) in enumerate(req_data["data"], 1):
        data[f'bot_{i}'] = name
        data[f'score_p_{i}'] = score
    return data
