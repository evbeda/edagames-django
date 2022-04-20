from auth_app.models import User
from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=30)
    date_tournament = models.DateTimeField(auto_now_add=True, verbose_name='Date')


class TournamentRegistration(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
