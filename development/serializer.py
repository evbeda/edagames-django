from rest_framework import serializers


class MatchSerializer(serializers.Serializer):
    game_id = serializers.CharField()
    tournament_id = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )
    data = serializers.ListField(
        child=serializers.ListField(max_length=2),
    )
