from auth_app.models import User
from django.db import models


class Championship(models.Model):
    name = models.CharField(max_length=30)
    tournament_bots = models.IntegerField(default=0)
    final_tournament = models.OneToOneField(
        'tournaments.Tournament',
        on_delete=models.CASCADE,
        related_name='championship_final'
    )

    def __str__(self):
        return f'{self.name} ({self.id})'


class Tournament(models.Model):
    TOURNAMENT_PENDING_STATUS = 'pending'
    TOURNAMENT_ACTIVE_STATUS = 'active'
    TOURNAMENT_FINISH_STATUS = 'finish'
    TOURNAMENT_STATUS = [
        (TOURNAMENT_PENDING_STATUS, 'Pending'),
        (TOURNAMENT_ACTIVE_STATUS, 'Active'),
        (TOURNAMENT_FINISH_STATUS, 'Finish'),
    ]

    name = models.CharField(max_length=30)
    date_tournament = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    status = models.CharField(
        max_length=8,
        choices=TOURNAMENT_STATUS,
        default=TOURNAMENT_PENDING_STATUS,
    )
    championship = models.ForeignKey(
        Championship,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name} ({self.id})'


class TournamentRegistration(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'{self.user.email} ({self.id})'


class FinalTournamentRegistration(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="final_tournament_registration"
    )
    championship = models.ForeignKey(
        Championship,
        on_delete=models.CASCADE,
        related_name="final_tournament_registration"
    )

    def __str__(self):
        return f'{self.user.email}, {self.championship.name} ({self.id})'
