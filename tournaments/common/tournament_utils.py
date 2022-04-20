from collections import defaultdict
from typing import List

from django.db.models import (
    Count,
    Sum,
)

from development.constants import (
    LOSS,
    TIE,
    WIN,
)
from development.models import MatchMembers


def get_tournament_results(tournament_id: int) -> List[dict]:
    """
    This method receives a tournament id and returns a list of dictionaries for each bot
    that has participated in the tournament.
    {
        bot name: {
            "total_match": the number of matches played:
            "total_match_won": the number of matches won:
            "total_match_tied": the number of matches tied:
            "total_match_lost": the number of matches lost:
            "total_score": the sum of scores made in all matches
        }
    }
    """
    results = calculate_match_results_by_player()
    results = add_score_to_results_and_total_matches(results)

    return results


def calculate_match_results_by_player():
    match_members_results = MatchMembers.objects.values_list(
        "bot__name",
        "match_result",
    ).filter(match__tournament=2).annotate(Count("bot_id"))

    results = defaultdict(lambda: {
        "total_match": 0,
        "total_match_won": 0,
        "total_match_tied": 0,
        "total_match_lost": 0,
        "total_score": 0,
    })
    for bot_name, match_result, quantity in match_members_results:
        if match_result == WIN:
            total_key = "total_match_won"
        elif match_result == TIE:
            total_key = "total_match_tied"
        elif match_result == LOSS:
            total_key = "total_match_lost"
        results[bot_name][total_key] = quantity
    return results


def add_score_to_results_and_total_matches(results):
    match_members_results = MatchMembers.objects.values_list(
        'bot__name',
        Sum('score')).filter(match__tournament=2).annotate(Count('score'))
    for bot_name, total_score, total_match in match_members_results:
        results[bot_name]["total_match"] = total_match
        results[bot_name]["total_score"] = total_score
    return results


def sort_position_table(table):
    table = convert_dict_to_tuples(table)
    return sorted(table, key=lambda x: (x[2], x[5], x[3]), reverse=True)


def convert_dict_to_tuples(table):
    return [
        (
            bot_name,
            match_result["total_match"],
            match_result["total_match_won"],
            match_result["total_match_tied"],
            match_result["total_match_lost"],
            match_result["total_score"],
        ) for bot_name, match_result in table.items()
    ]
