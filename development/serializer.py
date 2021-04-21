import io
from rest_framework.parsers import JSONParser
from model_serializer import MatchSerializer


# parse a stream into Python native datatype
def deserializing(data_server):
    stream = io.BytesIO(data_server)
    converted_data = JSONParser().parse(stream)
    # then we restore those native datatypes into a dictionary of validated data.
    serializer = MatchSerializer(data=converted_data)
    serializer.is_valid()
    # True
    serializer.validated_data
