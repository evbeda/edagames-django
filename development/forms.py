from django import forms
from .bot_handler import (
    get_data_users,
    get_online_bots,
    get_my_bots,
)


class ChallengeForm(forms.Form):
    def setup_bots_choices(self, user):
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
