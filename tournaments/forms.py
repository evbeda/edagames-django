from distutils.filelist import findall
from django import forms
import tournaments
from tournaments.common.form_utils import get_championships, get_tournaments_associated_with_championship

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


class FinalTournamentGeneratorForm(forms.Form):

    def setup_championship_choice(self):
        championships = get_championships()
        final_tournaments = get_tournaments_associated_with_championship()
        self.fields['championship_name'].choices = championships
        self.fields['final_tournament_name'].choices = final_tournaments

    championship_name = forms.ChoiceField(label='Championship', widget=forms.Select, choices=[])
    final_tournament_name = forms.ChoiceField(label='Final tournament', widget=forms.Select, choices=[])
