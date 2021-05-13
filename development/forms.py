from django import forms
import requests
from environment import get_env_variable

from auth_app.models import Bot


SERVER_URL = get_env_variable('SERVER_URL')
SERVER_PORT = get_env_variable('SERVER_PORT')


class ChallengeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        users = get_data_users()
        online_bots = get_online_bots(users)
        my_bots = get_my_bots(
            user,
            users,
        )
        self.fields['bot1'].choices = my_bots
        self.fields['bot2'].choices = online_bots

    bot1 = forms.ChoiceField(label='MyBots', widget=forms.Select, choices=[])
    bot2 = forms.ChoiceField(label='Online Bots', widget=forms.Select, choices=[])


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
