from auth_app.models import Bot
from development.models import (
    Match,
    MatchMembers,
)


def get_matches_of_connected_user(user):
    bots = Bot.objects.filter(user=user).values_list('id', flat=True)
    match_ids = MatchMembers.objects.filter(bot__in=bots).values_list('match_id', flat=True).distinct()
    return Match.objects.filter(id__in=match_ids)


def get_matches_results(matches):
    """
    Receives match objects and return the result of them
    - Input
        type: queryset
        value: [match1, match2, match3]
    - Output
        type: List[dict]
        value: [
            {
                "match": match1,
                "players": [
                    {
                        "name": "bot1",
                        "score": 2000,
                        "winner": true
                    },
                    {
                        "name": "bot2",
                        "score": 500,
                        "winner": false
                    }
                ]
            },
            ...
        ]
    """
    match_members = MatchMembers.objects.filter(match__in=matches)
    return [
        {
            'match': match,
            'players': get_match_players(match.id, match_members)
        }
        for match in matches
    ]


def get_match_players(match_id, match_members):
    return [
        {
            'name': match_member.bot.name,
            'score': match_member.score,
            'winner': match_member.winner,
        }
        for match_member in match_members
        if match_member.match.id == match_id
    ]
