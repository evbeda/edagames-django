from django.contrib import admin
from .models import (
    Championship,
    FinalTournamentRegistration,
    Tournament,
    TournamentRegistration,
)

admin.site.register(Championship)
admin.site.register(Tournament)
admin.site.register(TournamentRegistration)
admin.site.register(FinalTournamentRegistration)
