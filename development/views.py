from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from auth_app.models import Bot
from development.common.logs_utils import FilterLogs
from .common.match_utils import (
    get_matches_of_connected_user,
    get_matches_results,
)
from .common.match_result_text import (
    generate_text,
    generate_text_str
)
from development.forms import ChallengeForm
from development.server_requests import (
    get_logs,
    send_challenge,
)
from .encode_jwt import encode_data
from .forms import BotForm
from .models import Match
from .tables import BotTable


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
        debug_mode = bool(form.cleaned_data['debug_mode'])

        response = send_challenge(
            challenger=f"{bot1}",
            challenged=[f"{bot2}"],
            tournament_id="",
            debug_mode=debug_mode
        )
        if response.status_code == 200:
            messages.add_message(
                self.request,
                messages.INFO,
                'Challenge sent: '
                f'{bot1} VS {bot2}',
            )
        return super().form_valid(form)


class MatchListView(ListView):
    template_name = 'development/match_history.html'

    def get_queryset(self):
        matches = get_matches_of_connected_user(self.request.user)
        return get_matches_results(matches)


class MatchDetailsView(DetailView):
    template_name = 'development/match_details.html'
    model = Match

    def get_context_data(self, **kwargs):
        response = get_logs(
            game_id=self.object.game_id,
            page_token=self.request.GET.get('page'),
        )
        context = super(
            MatchDetailsView,
            self,
        ).get_context_data(**kwargs)

        data = response['details']
        filter_logs = FilterLogs(data)
        move_states = filter_logs.possible_states
        actions_kind = filter_logs.possible_actions
        context['move_states'] = move_states
        context['actions_kind'] = actions_kind
        context['data'] = data
        context['prev_page'] = response['prev']
        context['next_page'] = response['next']
        context['text'] = generate_text_str(data)
        return context


class NewMatchDetailsView(DetailView):
    template_name = 'development/new_match_details.html'
    model = Match

    def get_context_data(self, **kwargs):
        response = get_logs(
            game_id=self.object.game_id,
            page_token=self.request.GET.get('page'),
        )
        context = super(
            NewMatchDetailsView,
            self,
        ).get_context_data(**kwargs)
        details_for_front = {}
        for index, element in enumerate(response['details']):
            details_for_front[str(index)] = element

        data = response['details']
        filter_logs = FilterLogs(data)
        move_states = filter_logs.possible_states
        actions_kind = filter_logs.possible_actions

        context['move_states'] = move_states
        context['actions_kind'] = actions_kind
        context['data'] = response['details']
        context['text'] = generate_text(data)

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
    try:
        bot = Bot.objects.get(id=pk)
        if request.user.email != bot.name:
            bot.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Bot successfully removed'
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'The official bot cannot be removed'
            )
    except Bot.DoesNotExist:
        messages.add_message(
            request,
            messages.ERROR,
            'The bot does not exists'
        )
    return redirect('development:mybots')
