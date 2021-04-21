import io
from rest_framework.parsers import JSONParser
from model_serializer import MatchSerializer


def deserializing(data_server):
    # First we parse a stream into Python native datatypes
    stream = io.BytesIO(data_server)
    converted_data = JSONParser().parse(stream)
    # then we restore those native datatypes into a
    # fully populated object instance.
    serializer = MatchSerializer(data=converted_data)
    serializer.is_valid()
    # True
    serializer.validated_data
    # OrderedDict([])
    serializer.save()
    # <Match: Match object>
