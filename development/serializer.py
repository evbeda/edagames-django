from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['bot_one', 'bot_two', 'score_p_one', 'score_p_two', 'game_id']

    def create(self, validated_data):
        return Match.objects.create(**validated_data)
