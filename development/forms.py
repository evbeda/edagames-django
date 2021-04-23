from django import forms
import requests


SERVER_URL = 'http://127.0.0.1:5000'

my_bots = [
    ('0', 'brz'),
    ('1', 'pegaso'),
]
online_bots = [
    'brz',
    'pegaso',
    'sergi_pro',
    'andrew',
    'elenzo',
]


class ChallengeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bot1'].choices = my_bots
        self.fields['bot2'].choices = get_online_bots()

    bot1 = forms.ChoiceField(label='MyBots', widget=forms.RadioSelect, choices=[])
    bot2 = forms.ChoiceField(label='Online Bots', widget=forms.RadioSelect, choices=[])


def get_online_bots():
    try:
        bots_json = requests.get(
            '{}/users'.format(SERVER_URL),
        )
        data = bots_json.json()
        on_bots = [(str(i), bot) for i, bot in enumerate(data['users'])]
        return on_bots
    except Exception:
        on_bots = [(str(i), bot) for i, bot in enumerate(online_bots)]
        return on_bots
