from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = [
            'user_1',
            'user_2',
            'bot_1',
            'bot_2',
            'score_p_1',
            'score_p_2',
            'game_id',
            'tournament_id',
        ]

    def create(self, validated_data):
        return Match.objects.create(**validated_data)
