from edagames import settings
import requests
from typing import List
import json


def send_challenge(
    challenger: str,
    challenged: List[str],
    tournament_id: str = '',
):
    data = {
        "challenger": challenger,
        "challenged": challenged,
        "tournament_id": tournament_id,
    }
    return requests.post(
        f'{settings.SERVER_URL}:{settings.SERVER_PORT}/challenge',
        json=data,
    )


def get_one_page_logs(
    game_id: str,
    page_token: str,
):
    data = {
        "game_id": game_id,
        "page_token": page_token,
    }
    return requests.get(
        f'{settings.SERVER_URL}:{settings.SERVER_PORT}/match_details',
        params=data,
    )


def get_all_logs(game_id: str):
    first_page = get_one_page_logs(
        game_id,
        None,
    )
    first_page = json.loads(first_page)
    page_token = first_page['next']
    logs = [first_page]
    while page_token is not None:
        response = get_one_page_logs(
            game_id,
            page_token,
        )
        logs.append(json.loads(response))
    return logs
