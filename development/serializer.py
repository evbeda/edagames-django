from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
 
    def create(self, validated_data):
        return Match.objects.create(**validated_data)
