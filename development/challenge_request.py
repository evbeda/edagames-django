from environment import get_env_variable


SERVER_URL = get_env_variable('SERVER_URL')
SERVER_PORT = get_env_variable('SERVER_PORT')


def send_challenge(*args, **kwargs):
    data = {
        "challenger": "{}".format(kwargs['challenger']),
        "challenged": "{}".format(kwargs['challenged']),
        "challenge_id": "{}".format(kwargs['tournament_id']),
    }
    return kwargs['requests'].post(
        '{}:{}/challenge'.format(SERVER_URL, SERVER_PORT),
        json=data,
    )
