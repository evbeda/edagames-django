from rest_framework import serializers
from models import Match


class MatchSerializer(serializers.Serializer):
    bot1 = serializers.CharField(max_length=20)
    bot2 = serializers.CharField(max_length=20)
    score1 = serializers.IntegerField(max_lenght=4)
    score2 = serializers.IntegerField(max_lenght=4)
    board_id = serializers.CharField(max_length=300)

    def create(self, validated_data):
        return Match.objects.create(**validated_data)
