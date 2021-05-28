from django import forms
from .models import Tournament
# from development.bot_handler import (
#     get_users_data,
#     get_online_bots,
# )


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name',)


# class OnlineBotsForm(forms.Form):
#     def setup_bots_choices(self):
#         users = get_users_data()
#         online_bots = get_online_bots(users)
#         self.fields['bot2'].choices = online_bots

#     bot2 = forms.ChoiceField(label='Online Bots', widget=forms.Select, choices=[])
