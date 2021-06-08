from django.contrib import admin
from .models import (
    Challenge,
    Match,
    MatchMembers
)


admin.site.register(Challenge)
admin.site.register(Match)
admin.site.register(MatchMembers)
