import django_tables2 as tables
from .models import Match
from auth_app.models import Bot
from development import ACTIONS


class MatchTable(tables.Table):
    Details = tables.TemplateColumn(ACTIONS)

    class Meta:
        model = Match
        template_name = "django_tables2/bootstrap.html"
        fields = (
            'bot_1.name',
            'score_p_1',
            'bot_2.name',
            'score_p_2',
            'date_match',
        )


class BotTable(tables.Table):
    class Meta:
        model = Bot
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = (
            'name',
            'token',
        )
