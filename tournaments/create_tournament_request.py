from environment import get_env_variable
from itertools import combinations


SERVER_URL = get_env_variable('SERVER_URL')
SERVER_PORT = get_env_variable('SERVER_PORT')


def generate_combination(data1):
    a = []
    a = list(combinations(data1, 2))
    data = {
        'challenges': a
    }
    return kwargs['requests'].post(
        '{}:{}/create_tournament'.format(SERVER_URL, SERVER_PORT),
        json=data,
    )
