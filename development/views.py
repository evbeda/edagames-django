from django.views.generic.edit import FormView
from development.forms import ChallengeForm
from django.urls import reverse_lazy
from django.contrib import messages
import requests
from environment import get_env_variable
from django_tables2 import SingleTableView
from .models import Match
from .tables import MatchTable, BotTable
from auth_app.models import Bot
from .forms import BotForm
from .token import generate_token


SERVER_URL = get_env_variable('SERVER_URL')
SERVER_PORT = get_env_variable('SERVER_PORT')


class ChallengeView(FormView):
    form_class = ChallengeForm
    success_url = reverse_lazy('development:challenge')
    template_name = 'development/challenge.html'

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            form = ChallengeForm(data=self.request.POST)
        else:
            form = ChallengeForm()
        form.setup_bots_choices(self.request.user)

        return form

    def form_valid(self, form):
        option1 = int(form.cleaned_data['bot1'])
        option2 = int(form.cleaned_data['bot2'])
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


class MatchListView(SingleTableView):
    model = Match
    table_class = MatchTable
    template_name = 'development/match_history.html'

    def get_queryset(self):
        return Match.objects.filter(user_1=self.request.user) | Match.objects.filter(user_2=self.request.user)


class MyBotsView(SingleTableView):
    model = Bot
    table_class = BotTable
    template_name = 'development/my_bots.html'

    def get_queryset(self):
        return Bot.objects.filter(user=self.request.user)


class AddBotView(FormView):
    form_class = BotForm
    success_url = reverse_lazy('development:mybots')
    template_name = 'development/add_bot.html'

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            form = BotForm(data=self.request.POST)
        else:
            form = BotForm()
        return form

    def form_valid(self, form):
        new_bot = form.save(commit=False)
        new_bot.user = self.request.user
        new_bot.token = generate_token(new_bot.name)
        if not Bot.objects.filter(name=new_bot.name,).exists():
            new_bot.save()
            messages.add_message(
                self.request,
                messages.INFO,
                'Bot '
                '{} añadido exitosamente'.format(new_bot.name)
            )
        else:
            messages.add_message(
                self.request,
                messages.INFO,
                'No es posible crear este registro ,ya existe un bot con el nombre '
                '{}. Intente con un nombre diferente'.format(new_bot.name)
            )
        return super().form_valid(form)
