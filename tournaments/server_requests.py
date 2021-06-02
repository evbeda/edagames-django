from edagames import settings
import requests
from typing import List
from itertools import combinations


def generate_combination(
    bot_list: List[str],
    tournament_id: int,
):
    data = {
        'id': tournament_id,
        'challenges': list(combinations(bot_list, 2)),
    }
    return requests.post(
        f'{settings.SERVER_URL}:{settings.SERVER_PORT}/tournament',
        json=data,
    )
