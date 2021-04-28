from django.views.generic.edit import FormView
from development.forms import ChallengeForm
from django.views.generic.list import ListView
from .models import Match
from django.urls import reverse_lazy
from django.contrib import messages
import requests
from environment import get_env_variable


SERVER_URL = get_env_variable('SERVER_URL')
SERVER_PORT = get_env_variable('SERVER_PORT')


class ChallengeView(FormView):
    form_class = ChallengeForm
    success_url = reverse_lazy('development:challenge')

    def form_valid(self, form):
        option1 = form.cleaned_data['bot1']
        option2 = form.cleaned_data['bot2']
        bot1 = dict(form.fields['bot1'].choices)[option1]
        bot2 = dict(form.fields['bot2'].choices)[option2]

        data = {
            "challenger": "{}".format(bot1),
            "challenged": "{}".format(bot2),
            "challenge_id": "{}".format("1234"),
        }
        response = requests.post(
            '{}:{}/challenge'.format(SERVER_URL, SERVER_PORT),
            json=data,
        )
        if response.status_code == 200:
            messages.add_message(
                self.request,
                messages.INFO,
                'Challenge sent: '
                '{} VS {}'.format(bot1, bot2)
            )
        return super().form_valid(form)


class MatchListView(ListView):
    template_name = 'development/match_history.html'
    model = Match
