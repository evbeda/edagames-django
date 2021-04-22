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
    bot_one = models.CharField(max_length=30)
    bot_two = models.CharField(max_length=30)
    score_p_one = models.IntegerField()
    score_p_two = models.IntegerField()
    board_id = models.IntegerField()
    date_match = models.DateTimeField(auto_now_add=True)
