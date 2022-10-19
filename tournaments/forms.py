from distutils.filelist import findall
from django import forms
from tournaments.models import Championship
from tournaments.models import FinalTournamentRegistration
from tournaments.models import Tournament

from tournaments.models import TournamentRegistration, FinalTournamentRegistration


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


class FinalTournamentGeneratorForm(forms.Form):
    championship_name = forms.CharField(label="Championship", disabled=True,  widget=forms.HiddenInput(), required=False)
    final_tournament_name = forms.CharField(label="Final tournament", disabled=True,  widget=forms.HiddenInput(), required=False)
    
    # def setup_championship_and_tournament_names(self, championship_name, final_tournament_name):
    #     self.fields['championship_name'] = championship_name
    #     self.fields['final_tournament_name'] = final_tournament_name