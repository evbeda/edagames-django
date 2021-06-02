from edagames import settings
import requests
from typing import List
from itertools import combinations


def generate_combination(
    tournament_id: int,
    bot_list: List[str],
):
    data = {
        'tournament_id': tournament_id,
        'challenges': list(combinations(bot_list.split(sep=','), 2)),
    }
    return requests.post(
        f'{settings.SERVER_URL}:{settings.SERVER_PORT}/tournament',
        json=data,
    )
