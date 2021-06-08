from django.db import models
from auth_app.models import Bot
from tournaments.models import Tournament


class Challenge(models.Model):
    bot_challenger = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        blank=True,
        null=True,
    )
    bots_challenged = models.ManyToManyField(Bot)
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        blank=True,
        null=True,
    )


class Match(models.Model):
    game_id = models.CharField(max_length=50)
    date_match = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    match_members = models.ManyToManyField(
        Bot,
        through='MatchMembers',
    )
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class MatchMembers(models.Model):
    score = models.IntegerField()
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        null=True
    )
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        null=True
    )
