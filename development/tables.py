import django_tables2 as tables
from .models import Match


class MatchTable(tables.Table):
    class Meta:
        model = Match
        template_name = "django_tables2/bootstrap.html"
        fields = (
            'bot_one',
            'score_p_one',
            'bot_two',
            'score_p_two',
            'date_match',
        )
