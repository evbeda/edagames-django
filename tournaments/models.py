from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=30)
    date_tournament = models.DateTimeField(auto_now_add=True, verbose_name='Date')
