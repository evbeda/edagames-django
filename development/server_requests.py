from edagames import settings
import requests
from typing import List


def send_challenge(
    challenger: str,
    challenged: List[str],
    game_name: str,
    tournament_id: str = '',

):
    data = {
        "challenger": challenger,
        "challenged": challenged,
        "game_name": game_name,
        "tournament_id": tournament_id,
    }
    return requests.post(
        f'{settings.SERVER_URL}:{settings.SERVER_PORT}/challenge',
        json=data,
    )


def get_logs(
    game_id: str,
    page_token: str
):
    data = {
        "game_id": game_id,
        "page_token": page_token,
    }
    return requests.get(
        f'{settings.SERVER_URL}:{settings.SERVER_PORT}/match_details',
        params=data,
    ).json()
