from django.db import models
from auth_app.models import User
from auth_app.models import Bot


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
    bot_1 = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='bot_1',
        null=True
    )
    bot_2 = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='bot_2',
        null=True
    )
    score_p_1 = models.IntegerField(verbose_name='Score 1')
    score_p_2 = models.IntegerField(verbose_name='Score 2')
    game_id = models.CharField(max_length=50)
    date_match = models.DateTimeField(auto_now_add=True, verbose_name='Date')
