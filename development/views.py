from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from development.forms import ChallengeForm
from django.urls import reverse_lazy
from django.contrib import messages
import requests
from django_tables2 import SingleTableView
from .models import Match
from .tables import (
    BotTable,
    MatchTable,
)
from auth_app.models import Bot
from .forms import BotForm
from .encode_jwt import encode_data
from development.challenge_request import send_challenge


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

        response = send_challenge(
            requests=requests,
            challenger="{}".format(bot1),
            challenged=["{}".format(bot2)],
            tournament_id="",
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


DETAILS = {
    1: [
        {'player': 'P1', 'from_row': 1, 'to_row': 1},
        {'player': 'P2', 'from_row': 1, 'to_row': 1},
        {'player': 'P1', 'from_row': 1, 'to_row': 1},
        {'player': 'P2', 'from_row': 1, 'to_row': 1},
    ],
    2: [
        {'player': 'P1', 'from_row': 2, 'to_row': 2},
        {'player': 'P2', 'from_row': 2, 'to_row': 2},
        {'player': 'P1', 'from_row': 2, 'to_row': 2},
        {'player': 'P2', 'from_row': 2, 'to_row': 2},
    ],
    3: [
        {'player': 'P1', 'from_row': 3, 'to_row': 3},
        {'player': 'P2', 'from_row': 3, 'to_row': 3},
        {'player': 'P1', 'from_row': 3, 'to_row': 3},
        {'player': 'P2', 'from_row': 3, 'to_row': 3},
    ],
}


class MatchDetailView(DetailView):
    template_name = 'development/match_detail.html'

    def __init__(self, *args, **kwargs):
        super(MatchDetailView, self).__init__(*args, **kwargs)
        self.current_page = 1
        self.prev_page = 1
        self.next_page = 2
        self.pages = {
            1: '',
            2: '',
            3: '',
        }

    def get_queryset(self, *args, **kwargs):
        return Match.objects.filter(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        page = int(self.request.GET.get('page', '1'))
        if page in self.pages.keys():
            self.current_page = page
            self.prev_page = (
                page - 1
                if (page - 1) > 1
                else 1
            )
            self.next_page = page + 1

        # request logs server, if page=2 -> pages[2]

        context = super(
            MatchDetailView,
            self,
        ).get_context_data(**kwargs)
        context['data'] = DETAILS[int(page)]
        context['current_page'] = self.current_page
        context['prev_page'] = self.prev_page
        context['next_page'] = self.next_page
        return context


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
        new_bot.token = encode_data(
            key='user',
            value=new_bot.name,
        )
        if not Bot.objects.filter(name=new_bot.name,).exists():
            new_bot.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Bot '
                '{} successfully added'.format(new_bot.name)
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'It is not possible to create this record, a bot already exists with the name '
                '{}. Try a new name'.format(new_bot.name)
            )
            self.success_url = reverse_lazy('development:addbot')
        return super().form_valid(form)
