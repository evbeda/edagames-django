from django.contrib import admin
from .models import (
    Championship,
    Tournament,
    TournamentRegistration,
)

admin.site.register(Championship)
admin.site.register(Tournament)
admin.site.register(TournamentRegistration)
