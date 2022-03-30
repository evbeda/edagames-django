from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods
from development.forms import ChallengeForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import (
    Match,
    MatchMembers,
)
from .tables import (
    BotTable,
)
from auth_app.models import Bot
from .forms import BotForm
from .encode_jwt import encode_data
from development.server_requests import (
    get_logs,
    send_challenge,
)


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
            challenger=f"{bot1}",
            challenged=[f"{bot2}"],
            tournament_id="",
        )
        if response.status_code == 200:
            messages.add_message(
                self.request,
                messages.INFO,
                'Challenge sent: '
                f'{bot1} VS {bot2}',
            )
        return super().form_valid(form)


def get_matches_of_connected_user(user):
    bots = Bot.objects.filter(user=user).values_list('id', flat=True)
    match_ids = MatchMembers.objects.filter(bot__in=bots).values_list('match_id', flat=True).distinct()
    return Match.objects.filter(id__in=match_ids)


def get_matches_results(matches):
    """
    Receives match objects and return the result of them
    - Input
        type: queryset
        value: [match1, match2, match3]

    - Output
        type: List[dict]
        value: [
            {
                "match": match1,
                "players": [
                    {
                        "name": "bot1",
                        "score": 2000,
                        "winner": true
                    },
                    {
                        "name": "bot2",
                        "score": 500,
                        "winner": false
                    }
                ]
            },
            ...
        ]
    """
    match_members = MatchMembers.objects.filter(match__in=matches)
    matches_result = list()
    for match in matches:
        match_result = dict()
        match_result['match'] = match
        match_result['players'] = get_match_players(match.id, match_members)
        matches_result.append(match_result)
    return matches_result


def get_match_players(match_id, match_members):
    return [
        {
            'name': match_member.bot.name,
            'score': match_member.score,
            'winner': match_member.winner,
        }
        for match_member in match_members
        if match_member.match.id == match_id
    ]


class MatchListView(ListView):
    template_name = 'development/match_history.html'

    def get_queryset(self):
        matches = get_matches_of_connected_user(self.request.user)
        return get_matches_results(matches)


class MatchDetailsView(DetailView):
    template_name = 'development/match_details.html'

    def __init__(self, *args, **kwargs):
        super(MatchDetailsView, self).__init__(*args, **kwargs)
        # TODO
        self.prev_page = 1
        self.next_page = 2

    def get_queryset(self, *args, **kwargs):
        return Match.objects.filter(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        response = get_logs(
            game_id=self.object.game_id,
            page_token=None,
        )
        context = super(
            MatchDetailsView,
            self,
        ).get_context_data(**kwargs)
        response = response.json()
        context['data'] = response['details']
        context['prev_page'] = self.prev_page
        context['next_page'] = self.next_page
        return context


class MyBotsView(ListView):
    table_class = BotTable
    template_name = 'development/my_bots.html'

    def __init__(self, *args, **kwargs):
        super(MyBotsView, self).__init__(*args, **kwargs)

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


@require_http_methods(["POST"])
def delete_bot(request, pk):
    Bot.objects.get(id=pk).delete()
    messages.add_message(
        request,
        messages.SUCCESS,
        'Bot successfully removed'
    )
    return redirect('development:mybots')
