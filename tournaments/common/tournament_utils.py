from collections import defaultdict
from itertools import combinations
from random import shuffle
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
from auth_app.models import Bot, User
from development.models import Challenge, MatchMembers
from tournaments.models import Championship, FinalTournamentRegistration, Tournament


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
    results = calculate_match_results_by_player(tournament_id)
    results = add_score_to_results_and_total_matches(results, tournament_id)

    return results


def calculate_match_results_by_player(tournament_id):
    match_members_results = MatchMembers.objects.values_list(
        "bot__name",
        "match_result",
    ).filter(match__tournament=tournament_id).annotate(Count("bot_id"))

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


def add_score_to_results_and_total_matches(results, tournament_id):
    match_members_results = MatchMembers.objects.values_list(
        'bot__name',
        Sum('score')).filter(match__tournament=tournament_id).annotate(Count('score'))
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


def register_bots_to_final_tournament(champ: Championship, max_bot_finalist: int):
    # get the tournaments
    tournaments_list = Tournament.objects.filter(championship=champ.pk)
    # get list of all bots that have been in the tournaments
    bot_that_participated = []
    for tournament in tournaments_list:
        bot_that_participated.append(
            sort_position_table(
                get_tournament_results(
                    tournament.id)))
    # get the first n bots and register them to the final
    top_bots = bot_that_participated[0][:max_bot_finalist]
    finalist_users = []
    for bot in top_bots:
        user = User.objects.get(email=bot[0])
        finalist_users.append(user)
    return finalist_users


def create_registrations_and_challenges_for_final_tournament(
        championship: Championship,
        final_tournament: Tournament,
        max_bot_finalist):

    tournaments_participants = register_bots_to_final_tournament(championship, max_bot_finalist)
    tournament_registrations = [
        FinalTournamentRegistration.objects.create(
            user=user, championship=championship) for user in tournaments_participants]
    shuffle(tournament_registrations)
    bots = [
        Bot.objects.get(user=tournament_registration.user, name=tournament_registration.user.email)
        for tournament_registration
        in tournament_registrations
    ]
    challenges = combinations(bots, 2)
    for bot_challenger, bots_challenged in challenges:
        challenge = Challenge.objects.create(
            bot_challenger=bot_challenger,
            tournament=final_tournament,
        )
        challenge.bots_challenged.add(bots_challenged)
