from django.contrib import admin
from .models import (
    Tournament,
    TournamentRegistration,
    Championship,
)


admin.site.register(Tournament)
admin.site.register(TournamentRegistration)
admin.site.register(Championship)
