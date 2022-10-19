from django import forms

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


class ChampionshipCreateForm(forms.Form):
    championship_name = forms.CharField(label='name', required=True)
    tournament_bots = forms.IntegerField(label='Finalist Bots per Tournament', required=True)
    max_players = forms.IntegerField(label='maxPlayers', required=True)
