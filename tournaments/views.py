from itertools import combinations
from random import shuffle

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from auth_app.models import Bot
from development.models import Challenge
from tournaments.common.tournament_utils import (
    get_tournament_results,
    sort_position_table,
)
from tournaments.models import (
    Tournament,
    TournamentRegistration,
)
from tournaments.server_requests import generate_combination
from tournaments.forms import (
    TournamentForm,
    TournamentGeneratorForm,
)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class RegistrationTournamentView(LoginRequiredMixin, TemplateView):
    template_name = 'tournaments/tournament_registration.html'

    def registration_exists(self):
        return TournamentRegistration.objects.filter(
            user=self.request.user,
        ).exists()

    def post(self, request, *args, **kwargs):
        if self.registration_exists():
            TournamentRegistration.objects.get(user=self.request.user).delete()
        else:
            TournamentRegistration.objects.create(user=self.request.user)
        return self.get(request, *args, **kwargs)

    def get_context_data(self):
        already_registered = self.registration_exists()
        context = {
            'already_registered': already_registered,
        }
        return context


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
            Tournament.objects.create(name=data[0], status=Tournament.TOURNAMENT_ACTIVE_STATUS)
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


class TournamentGeneratorView(StaffRequiredMixin, FormView):
    form_class = TournamentGeneratorForm
    success_url = reverse_lazy('tournaments:tournaments_history')
    template_name = 'tournaments/tournament_generator.html'

    def create_tournaments(self, tournament_name, max_players):
        tournament_registrations_qs = TournamentRegistration.objects.all()
        tournament_registrations = list(tournament_registrations_qs)
        shuffle(tournament_registrations)
        tournament_count = len(tournament_registrations) // max_players
        if len(tournament_registrations) % max_players > 0:
            tournament_count += 1
        for tournament_index in range(0, tournament_count):
            tournament = Tournament.objects.create(name='{} #{}'.format(tournament_name, tournament_index + 1))
            registration_index = tournament_index * max_players
            bots = [
                Bot.objects.get(user=tournament_registration.user, name=tournament_registration.user.email)
                for tournament_registration
                in tournament_registrations[registration_index: registration_index + max_players]
            ]
            challenges = combinations(bots, 2)
            for bot_challenger, bots_challenged in challenges:
                challenge = Challenge.objects.create(
                    bot_challenger=bot_challenger,
                    tournament=tournament,
                )
                challenge.bots_challenged.add(bots_challenged)

    def form_valid(self, form):
        tournament_name = form.cleaned_data['tournament_name']
        if not Tournament.objects.filter(name=tournament_name).exists():
            max_players = form.cleaned_data['max_players']
            self.create_tournaments(tournament_name, max_players)
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'It is not possible to create this record, a tournament already exists with the name '
                '{}. Try a new name'.format(tournament_name)
            )
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['registrations'] = TournamentRegistration.objects.all()
        return context


class TournamentListView(ListView):
    template_name = 'tournaments/tournaments_history.html'

    def get_queryset(self):
        return Tournament.objects.exclude(status=Tournament.TOURNAMENT_PENDING_STATUS).order_by("-date_tournament")


class PendingTournamentListView(LoginRequiredMixin, ListView):
    template_name = 'tournaments/tournaments_pending.html'

    def get_queryset(self):
        return Tournament.objects.filter(status=Tournament.TOURNAMENT_PENDING_STATUS).order_by("-date_tournament")


class TournamentResultsView(ListView):
    template_name = 'tournaments/tournament_results.html'

    def get_queryset(self, *args, **kwargs):
        return sort_position_table(get_tournament_results(self.kwargs.get('pk')))
