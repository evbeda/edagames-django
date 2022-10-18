from itertools import combinations
from random import shuffle

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from tournaments.models import Championship, FinalTournamentRegistration
from auth_app.models import User


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
from tournaments.server_requests import (
    generate_combination_and_start_tournament,
    start_tournament,
)
from tournaments.forms import (
    FinalTournamentGeneratorForm,
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
            if not Bot.objects.filter(user=self.request.user, name=self.request.user.email).exists():
                Bot.objects.create(user=self.request.user, name=self.request.user.email)

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
        self.validation_data(form)  # TODO
        tournament_name = form.cleaned_data['tournament']
        bots_selected = form.cleaned_data['bots_selected'].split(sep=',')
        if not Tournament.objects.filter(name=tournament_name).exists():
            tournament = Tournament.objects.create(name=tournament_name, status=Tournament.TOURNAMENT_ACTIVE_STATUS)
            response = generate_combination_and_start_tournament(tournament.id, bots_selected)

            if response.status_code == 200:
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    'Tournament '
                    '{} successfully added'.format(tournament_name)
                )
            else:
                Tournament.objects.filter(name=tournament_name).delete()
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    'Tournament {} was not created. '
                    'Server is not receiving tournaments, '
                    'or maybe can not create them at this moment. '
                    'Please verify everything is working '
                    'and try again. '.format(tournament_name)
                )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'It is not possible to create this record, a tournament already exists with the name '
                '{}. Try a new name'.format(tournament_name)
            )
            self.success_url
        return super().form_valid(form)

    def validation_data(self, form):
        data = []
        data.append(form.cleaned_data['tournament'])
        data.append(form.cleaned_data['bots_selected'])
        data.append(form.cleaned_data['bots'])
        return (data)


class TournamentGeneratorView(StaffRequiredMixin, FormView):
    form_class = TournamentGeneratorForm
    success_url = reverse_lazy('tournaments:tournaments_pending')
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
        registrations = TournamentRegistration.objects.all()
        context['registrations'] = registrations
        context['registrations_count'] = len(registrations)
        return context


class TournamentListView(ListView):
    template_name = 'tournaments/tournaments_history.html'

    def get_queryset(self):
        return Tournament.objects.exclude(status=Tournament.TOURNAMENT_PENDING_STATUS).order_by("-date_tournament")


class PendingTournamentListView(LoginRequiredMixin, ListView):
    template_name = 'tournaments/tournaments_pending.html'

    def get_queryset(self):
        return Tournament.objects.filter(status=Tournament.TOURNAMENT_PENDING_STATUS).order_by("-date_tournament")

    def post(self, *args, **kwargs):
        if 'tournament' in self.request.GET:
            tournament_id = int(self.request.GET['tournament'])
            tournament = Tournament.objects.get(pk=tournament_id)
            challenges = Challenge.objects.filter(tournament_id=tournament_id)
            challenges_bots = []
            for challenge in challenges:
                bots_selected = [challenge.bot_challenger.name]
                for bots_challenge in challenge.bots_challenged.all():
                    bots_selected.append(bots_challenge.name)
                challenges_bots.append(tuple(bots_selected))
            start_tournament(tournament_id, challenges_bots)
            tournament.status = Tournament.TOURNAMENT_ACTIVE_STATUS
            tournament.save()

        return self.get(*args, **kwargs)


class TournamentResultsView(ListView):
    template_name = 'tournaments/tournament_results.html'

    def get_queryset(self, *args, **kwargs):
        return sort_position_table(get_tournament_results(self.kwargs.get('pk')))


@require_http_methods(["POST"])
def delete_tournament(request, pk):
    try:
        tournament = Tournament.objects.get(id=pk)
        tournament.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Tournament successfully removed'
        )
    except Tournament.DoesNotExist:
        messages.add_message(
            request,
            messages.ERROR,
            'The tournament does not exists'
        )
    return redirect('tournaments:tournaments_pending')


class CreateFinalTournamentView(StaffRequiredMixin, FormView):
    form_class = FinalTournamentGeneratorForm
    success_url = reverse_lazy('tournaments:tournaments_pending')
    template_name = 'tournaments/final_tournament_generator.html'

    def create_final_tournament(self, championship: Championship, final_tournament: Tournament, max_bot_finalist):
        tournaments_participants = _register_bots_to_final_tournament(championship, max_bot_finalist)
        tournament_registrations = [FinalTournamentRegistration.objects.create(user=user, championship=championship) for user in tournaments_participants]
        shuffle(tournament_registrations)
        bots = [
            Bot.objects.get(user=tournament_registration.user, name=tournament_registration.user.email)
            for tournament_registration
            in tournament_registrations
        ]
        challenges = combinations(bots, 2)
        for bot_challenger, bots_challenged in challenges:
            challenge = Challenge.objects.create(
                bot_challenger=bot_challenger,
                tournament=final_tournament,
            )
            challenge.bots_challenged.add(bots_challenged)

    def form_valid(self, form):
        final_tournament_name = form.cleaned_data['final_tournament_name']
        championship_name = form.cleaned_data['championship_name']
        championship = Championship.objects.get(name=championship_name)
        final_tournament = Tournament.objects.get(pk=championship.final_tournament)
        if not Tournament.objects.filter(name=final_tournament_name).exclude(status=Tournament.TOURNAMENT_FINISH_STATUS):
            self.create_final_tournament(championship, final_tournament, championship.tournament_bots)
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'It is not possible to create this record, a tournament already exists with the name '
                '{}. Try a new name'.format(final_tournament_name)
            )
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        registrations = FinalTournamentRegistration.objects.all()
        context['registrations'] = registrations
        context['registrations_count'] = len(registrations)
        return context
    
def _register_bots_to_final_tournament(champ: Championship, max_bot_finalist: int):
    # get the tournaments
    tournaments_list = Tournament.objects.filter(championship=champ.pk)
    # get list of all bots that have been in the tournaments
    bot_that_participated = [
        sort_position_table(
            get_tournament_results(tournament_id)
        ) for tournament_id in tournaments_list
        ]
    # get the first n bots and register them to the final
    top_bots = bot_that_participated[:max_bot_finalist]
    finalist_bots = [bot[0] for bot in top_bots]
    finalist_users = []
    for bot in finalist_bots:
        user = User.objects.get(email=bot)
        finalist_users.append(user)
    return finalist_bots
    