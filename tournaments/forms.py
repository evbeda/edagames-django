from django import forms
from tournaments.common.form_utils import get_championships

from tournaments.models import TournamentRegistration


class TournamentForm(forms.Form):
    tournament = forms.CharField(label='name')
    bots_selected = forms.CharField(label='botsSelected', widget=forms.HiddenInput(), required=False)
    bots = forms.ChoiceField(label='Bots', widget=forms.HiddenInput(), choices=[], required=False)

    def setup_bots_choices(self):
        users_registration = TournamentRegistration.objects.all().order_by('user__email')
        self.fields['bots'].choices = enumerate([registration.user.email for registration in users_registration])


class TournamentGeneratorForm(forms.Form):
    tournament_name = forms.CharField(label='name', required=True)
    max_players = forms.IntegerField(label='maxPlayers', required=True)


class ChampionshipGeneratorForm(forms.Form):
    championship_name = forms.CharField(label='championship name', required=True)
    finalist_users_per_tournament = forms.IntegerField(label='finalist users per tournament', required=True)
    max_players = forms.IntegerField(label='max players per tournament', required=True)


class FinalTournamentGeneratorForm(forms.Form):
    championship_name = forms.ChoiceField(label='Championship', widget=forms.Select(), choices=[])

    def setup_championship_choice(self):
        championships = get_championships()
        self.fields['championship_name'].choices = championships
