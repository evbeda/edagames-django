from django import forms


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
    bot1 = forms.ChoiceField(label='MyBots', widget=forms.RadioSelect, choices=my_bots)
    bot2 = forms.ChoiceField(label='Online Bots', widget=forms.RadioSelect, choices=online_bots)
