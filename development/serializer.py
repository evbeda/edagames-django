from rest_framework import serializers
from models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['bot1', 'bot2', 'score1', 'score2', 'board_id']

    def create(self, validated_data):
        return Match.objects.create(**validated_data)
