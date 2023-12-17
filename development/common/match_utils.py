from django.db import transaction

from auth_app.models import Bot
from development.models import (
    Match,
    MatchMembers,
)


def get_matches_of_connected_user(user):
    bots = Bot.objects.filter(user=user).values_list('id', flat=True)
    match_ids = MatchMembers.objects.filter(bot__in=bots).values_list('match_id', flat=True).distinct()
    return Match.objects.filter(id__in=match_ids).order_by('-date_match')


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
            'winner': match_member.match_result > 0,
            'match_result': match_member.match_result,
        }
        for match_member in match_members
        if match_member.match.id == match_id
    ]


@transaction.atomic
def save_match(match_info):
    match = Match.objects.create(
        game_id=match_info['game_id'],
        tournament_id=match_info['tournament_id'],
    )
    match_result = calculate_match_result(match_info['data'])
    match_members = generate_match_members(match, match_info['data'], match_result)
    MatchMembers.objects.bulk_create(match_members)


def generate_match_members(match, match_data, match_result):
    match_members = []
    for name, score in match_data:
        if name is match_result["winner"]:
            result = 2
        elif name in match_result["ties"]:
            result = 1
        else:
            result = 0
        match_members.append(
            MatchMembers(
                bot=Bot.objects.get(name=name),
                score=score,
                match=match,
                match_result=result,
            )
        )
    return match_members


def calculate_match_result(match_data: list) -> dict:
    """
    Receives a list of [bot_name, score] items and look for
    winner and players that are tied.
    - Input:
        [
            ['bot_2', 123],
            ['bot_1', 555],
            ['bot_3', 441],
            ['bot_5', 324],
        ]
    - Oupput:
        {
            "winner": 'bot_1',
            "ties": []
        }
    """
    match_data.sort(key=lambda x: x[1], reverse=True)
    highest_score = match_data[0][1]
    winner = get_winner(match_data, highest_score)
    ties = []
    if not winner:
        ties = get_ties(match_data, highest_score)
    return {
        "winner": winner,
        "ties": ties,
    }


def get_winner(match_data, highest_score):
    winner = None
    if not sum(score.count(highest_score) for score in match_data) > 1:
        winner = match_data[0][0]
    return winner


def get_ties(match_data, highest_score):
    return [
        player for player, score in match_data
        if score == highest_score
    ]
