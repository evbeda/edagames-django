from django.contrib import admin
from .models import (
    Tournament,
    TournamentRegistration,
)


admin.site.register(Tournament)
admin.site.register(TournamentRegistration)
