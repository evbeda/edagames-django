from django.db import models
from auth_app.models import User


class Match(models.Model):
    user_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_one',
        null=True
    )
    user_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_two',
        null=True
    )
    bot_one = models.CharField(max_length=30, verbose_name='Player 1')
    bot_two = models.CharField(max_length=30, verbose_name='Player 2')
    score_p_one = models.IntegerField(verbose_name='Score 1')
    score_p_two = models.IntegerField(verbose_name='Score 2')
    bot_1 = models.CharField(max_length=30)
    bot_2 = models.CharField(max_length=30)
    score_p_1 = models.IntegerField()
    score_p_2 = models.IntegerField()
    game_id = models.CharField(max_length=50)
    date_match = models.DateTimeField(auto_now_add=True, verbose_name='Date')
