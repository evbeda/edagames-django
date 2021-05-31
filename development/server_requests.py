from development import (
    SERVER_PORT,
    SERVER_URL,
)


def send_challenge(*args, **kwargs):
    data = {
        "challenger": kwargs['challenger'],
        "challenged": kwargs['challenged'],
        "tournament_id": kwargs['tournament_id'],
    }
    return kwargs['requests'].post(
        '{}:{}/challenge'.format(SERVER_URL, SERVER_PORT),
        json=data,
    )


def get_logs(*args, **kwargs):
    data = {
        "game_id": kwargs['game_id'],
        "page_token": kwargs['page_token'],
    }
    return kwargs['requests'].get(
        '{}:{}/match_details'.format(SERVER_URL, SERVER_PORT),
        params=data,
    )
