from edagames import settings
import requests
from typing import List
from itertools import combinations


def generate_combination_and_start_tournament(
    tournament_id: int,
    bot_list: List[str],
):
    return start_tournament(tournament_id, list(combinations(bot_list, 2)))


def start_tournament(
    tournament_id: int,
    challenges: List[tuple],
):
    data = {
        'tournament_id': str(tournament_id),
        'challenges': challenges,
    }
    return requests.post(
        f'{settings.SERVER_URL}:{settings.SERVER_PORT}/tournament',
        json=data,
    )
