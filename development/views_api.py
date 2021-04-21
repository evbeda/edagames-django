from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from serializer import MatchSerializer
from models import Match


@csrf_exempt
def match_list(request):
    # pendiente de definir con Nacho
    if request.method == 'GET':
        matchs = Match.objects.all()
        return matchs

    elif request.method == 'POST':
        # restore those native datatypes into a
        # fully populated object instance
        data = JSONParser().parse(request)
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # <Match: Match object>
            # Se ejecutan los metodos que cree
            # En mi caso solo create
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
