from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from development.serializer import (
    MatchSerializer,
)
from development.common.match_utils import save_match


@csrf_exempt
def match_list(request):
    """
    Recieve data from server and validate data for Match class

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
        import logging
        logging.warn(f"POST match {dic_data}")
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
