from .models import Tournament
from .forms import TournamentForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)


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
        if form.is_valid():
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
