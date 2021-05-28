from django import forms
from auth_app.models import Bot


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('name',)
