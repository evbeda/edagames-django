from auth_app.models import User
from django.db import models


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
