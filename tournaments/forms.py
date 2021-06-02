from django import forms
from auth_app.models import Bot


class TournamentForm(forms.Form):
    tournament = forms.CharField(label='name')
    bots_selected = forms.CharField(label='botsSelected', widget=forms.HiddenInput(), required=False)
    bots = forms.ChoiceField(label='Bots', widget=forms.HiddenInput(), choices=[], required=False)

    def setup_bots_choices(self):
        bots = Bot.objects.all()
        self.fields['bots'].choices = enumerate([bot.name for bot in bots])
