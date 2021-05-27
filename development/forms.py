from django import forms
from .bot_handler import (
    get_users_data,
    get_online_bots,
    get_my_bots,
)
from auth_app.models import Bot
import re


class ChallengeForm(forms.Form):
    def setup_bots_choices(self, user):
        users = get_users_data()
        online_bots = get_online_bots(users)
        my_bots = get_my_bots(
            user,
            users,
        )
        self.fields['bot1'].choices = my_bots
        self.fields['bot2'].choices = online_bots

    bot1 = forms.ChoiceField(label='MyBots', widget=forms.Select, choices=[])
    bot2 = forms.ChoiceField(label='Online Bots', widget=forms.Select, choices=[])


class BotForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Bot
        fields = ('name',)

    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        if not re.match("[A-Za-z0-9]*$", name):
            raise forms.ValidationError('Name cannot contains symbols or spaces')
        return name
