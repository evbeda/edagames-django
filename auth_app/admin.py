from django.contrib import admin
from .models import (
    Bot,
    User,
)


admin.site.register(
    User,
    Bot,
)
