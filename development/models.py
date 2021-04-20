from django.db import models


class Match(models.Model):
    player_one = models.CharField(max_length=30)
    player_two = models.CharField(max_length=30)
    score_p_one = models.IntegerField()
    score_p_two = models.IntegerField()
    date = models.DateTimeField()
