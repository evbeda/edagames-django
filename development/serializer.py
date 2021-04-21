import io
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from models import Match


# parse a stream into Python native datatype
def deserializing(data_server):
    stream = io.BytesIO(data_server)
    converted_data = JSONParser().parse(stream)


    # then we restore those native datatypes into a dictionary of validated data.
    serializer = MatchSerializer(data=converted_data)
    serializer.is_valid()
    # True
    serializer.validated_data
    comment = serializer.save()


class MatchSerializer(serializers.Serializer):
    bot1 = serializers.CharField(max_length=20)
    bot2 = serializers.CharField(max_length=20)
    score1 = serializers.IntegerField(max_lenght=4)
    score2 = serializers.IntegerField(max_lenght=4)
    board_id = serializers.CharField(max_length=300)

    def create(self, validated_data):
        return Match.objects.create(**validated_data)
