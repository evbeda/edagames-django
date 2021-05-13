import requests
from environment import get_env_variable

from auth_app.models import Bot


SERVER_URL = get_env_variable('SERVER_URL')
SERVER_PORT = get_env_variable('SERVER_PORT')


def get_data_users():
    try:
        bots_json = requests.get(
            '{}:{}/users'.format(SERVER_URL, SERVER_PORT),
        )
        data = bots_json.json()
        users = data['users']
    except Exception:
        users = []

    return users


def get_online_bots(users):
    return enumerate(users)


def get_my_bots(user_online, online_bots):
    queryset = Bot.objects.filter(user=user_online)
    bot_names = [bot.name for bot in queryset]

    return enumerate(set(bot_names) & set(online_bots))
