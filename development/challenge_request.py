from environment import get_env_variable


SERVER_URL = get_env_variable('SERVER_URL')
SERVER_PORT = get_env_variable('SERVER_PORT')


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
