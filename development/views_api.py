from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from development.serializer import MatchSerializer


@csrf_exempt
def match_list(request):
    # if request.method == 'GET':
    # matchs = Match.objects.all()
    # serializer = MatchSerializer(matchs, many=True)
    # return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
