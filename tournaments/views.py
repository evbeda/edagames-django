from .models import Tournament
from .server_requests import generate_combination
from .forms import TournamentForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic.list import ListView
from development.models import MatchMembers


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class CreateTournamentView(StaffRequiredMixin, FormView):
    form_class = TournamentForm
    success_url = reverse_lazy('tournaments:create_tournament')
    template_name = 'tournaments/create_tournaments.html'

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            form = TournamentForm(data=self.request.POST)
        else:
            form = TournamentForm()
        form.setup_bots_choices()
        return form

    def form_valid(self, form):
        data = []
        data = self.validation_data(form)
        if not Tournament.objects.filter(name=data[0]).exists():
            Tournament.objects.create(name=data[0])
            response = generate_combination(data[0], data[1])

            if response.status_code == 200:
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    'Tournament '
                    '{} successfully added'.format(data[0])
                )
            else:
                Tournament.objects.filter(name=data[0]).delete()
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    'Tournament {} was not created. '
                    'Server is not receiving tournaments, '
                    'or maybe can not create them at this moment. '
                    'Please verify everything is working '
                    'and try again. '.format(data[0])
                )
                self.success_url

        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'It is not possible to create this record, a tournament already exists with the name '
                '{}. Try a new name'.format(data[0])
            )
            self.success_url
        return super().form_valid(form)

    def validation_data(self, form):
        data = []
        data.append(form.cleaned_data['tournament'])
        data.append(form.cleaned_data['bots_selected'])
        data.append(form.cleaned_data['bots'])
        return(data)


class TournamentListView(ListView):
    template_name = 'tournaments/tournaments_history.html'

    def get_queryset(self):
        return Tournament.objects.all().order_by("-date_tournament")


def get_tournament_results(tournament_id):
    results = []
    tournament_match_members = MatchMembers.objects.filter(
        match__tournament=tournament_id,
    ).order_by('bot')
    result_bot = None
    total_match = 0
    total_match_won = 0
    total_score = 0
    for bot_match_member in tournament_match_members:
        if result_bot != bot_match_member.bot.name:
            if result_bot is not None:
                results.append({
                    'bot': result_bot,
                    'total_match': total_match,
                    'total_match_won': total_match_won,
                    'total_score': total_score,
                })
            total_match = 0
            total_match_won = 0
            total_score = 0
            result_bot = bot_match_member.bot.name
        total_match += 1
        if bot_match_member.winner:
            total_match_won += 1
        total_score += bot_match_member.score
    if result_bot is not None:
        results.append({
            'bot': result_bot,
            'total_match': total_match,
            'total_match_won': total_match_won,
            'total_score': total_score,
        })
    return results


class TournamentResultsView(ListView):
    template_name = 'tournaments/tournament_results.html'

    def get_queryset(self, *args, **kwargs):
        results = get_tournament_results(self.kwargs.get('pk')).sort(key=lambda x: x['total_match_won'], reverse=True)
        return results
