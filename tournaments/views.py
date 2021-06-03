from .models import Tournament
from .forms import TournamentForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from development.models import Match


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
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Tournament '
                '{} successfully added'.format(data[0])
            )
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


players = [
    {
        "pos": 1,
        "name": "brz",
        "points": 57,
        "matches_played": 20,
        "matches_win": 19,
        "matches_lose": 1,
        "score_in_favor": 58590,
    },
    {
        "pos": 2,
        "name": "juan",
        "points": 45,
        "matches_played": 20,
        "matches_win": 15,
        "matches_lose": 5,
        "score_in_favor": 42120,
    },
    {
        "pos": 3,
        "name": "carlos",
        "points": 12,
        "matches_played": 20,
        "matches_win": 4,
        "matches_lose": 16,
        "score_in_favor": 11542,
    },
    {
        "pos": 4,
        "name": "carlos",
        "points": 12,
        "matches_played": 20,
        "matches_win": 4,
        "matches_lose": 16,
        "score_in_favor": 11542,
    },
    {
        "pos": 5,
        "name": "flor",
        "points": 12,
        "matches_played": 20,
        "matches_win": 4,
        "matches_lose": 16,
        "score_in_favor": 11542,
    },
    {
        "pos": 6,
        "name": "esteban",
        "points": 12,
        "matches_played": 20,
        "matches_win": 4,
        "matches_lose": 16,
        "score_in_favor": 11542,
    },
    {
        "pos": 7,
        "name": "brenda",
        "points": 9,
        "matches_played": 20,
        "matches_win": 3,
        "matches_lose": 17,
        "score_in_favor": 666,
    },
    {
        "pos": 8,
        "name": "antony",
        "points": 0,
        "matches_played": 20,
        "matches_win": 0,
        "matches_lose": 20,
        "score_in_favor": -14005,
    },
]


class TournamentResult(ListView):
    template_name = 'tournaments/tournament_results.html'

    def get_queryset(self, *args, **kwargs):
        return Match.objects.filter(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(
            TournamentResult,
            self,
        ).get_context_data(**kwargs)
        context['players'] = players
        return context
