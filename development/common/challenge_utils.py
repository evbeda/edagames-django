from django.db import transaction

from development.models import (
    Bot,
    Challenge,
)
from tournaments.models import Tournament


@transaction.atomic
def save_challenge(bot_challenger_name, bots_challenged_names, tournament):
    bot_challenger = Bot.objects.filter(name=bot_challenger_name).first()
    bots_challenged = Bot.objects.filter(name__in=bots_challenged_names)
    if tournament:
        tournament = Tournament.objects.filter(name=tournament).first()

    challenge = Challenge.objects.create(
        bot_challenger=bot_challenger,
        tournament=tournament,
    )
    challenge.bots_challenged.set(bots_challenged)
