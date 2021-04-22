from django import forms
import requests
from rest_framework.parsers import JSONParser

PLATFORM_URL = 'http://localhost:5000/users'

my_bots = [
    ('1', 'brz'),
    ('2', 'pegaso'),
]
online_bots = [
    ('1', 'brz'),
    ('2', 'pegaso'),
    ('3', 'sergi_pro'),
    ('4', 'andrew'),
    ('5', 'elenzo'),
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
        bots_json = requests.get(PLATFORM_URL)
        data = JSONParser().parse(bots_json)
        return data['users']
    except Exception:
        return online_bots
