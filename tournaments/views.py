from django.views.generic.edit import FormView
from .models import Tournament
from .forms import TournamentForm
from django.urls import reverse_lazy
from django.contrib import messages
from development.encode_jwt import encode_data
from development.bot_handler import (
    get_users_data,
    get_online_bots,
)


class AddBotView(FormView):
    form_class = TournamentForm
    users = get_users_data()
    online_bots = get_online_bots(users)
    success_url = reverse_lazy('tournaments:tournament')
    template_name = 'tournaments/create_tournaments.html'

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            form = TournamentForm(data=self.request.POST)
        else:
            form = TournamentForm()
        return form

    def form_valid(self, form):
        new_tournament = form.save(commit=False)
        new_tournament.user = self.request.user
        new_tournament.token = encode_data(
            key='user',
            value=new_tournament.name,
        )
        if not Tournament.objects.filter(name=new_tournament.name,).exists():
            new_tournament.save()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                'Tournament '
                '{} successfully added'.format(new_tournament.name)
            )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                'It is not possible to create this record, a tournament already exists with the name '
                '{}. Try a new name'.format(new_tournament.name)
            )
            self.success_url = reverse_lazy('tournaments:tournament')
        return super().form_valid(form)
