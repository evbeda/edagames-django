import django_tables2 as tables
from auth_app.models import Bot


class BotTable(tables.Table):
    class Meta:
        model = Bot
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = (
            'name',
            'token',
        )
