from django.views.generic.edit import FormView
from auth_app.models import Bot
from .models import Tournament
from .forms import TournamentForm
from django.urls import reverse_lazy
from django.contrib import messages
from development.encode_jwt import encode_data
from development.bot_handler import (
    get_users_data,
    get_online_bots,
)
from django.shortcuts import render


class AddBotView(FormView):
    form_class = TournamentForm
    users = get_users_data()
    online_bots = get_online_bots(users)
    success_url = reverse_lazy('tournaments:tournament')
    template_name = 'tournaments/create_tournaments.html'

    # def search(request):
    #     objs = Bot.objects.all()
    #     if request.method == 'POST':
    #         form = TournamentForm(request.POST)
    #     else:
    #         form = TournamentForm()
    #     return render(request, 'SpotMe/search.html', {'form' : form, 'objs': objs})
    # def get_context_data(self, **kwargs):
    #     context = super(InventoryListView, self).get_context_data(**kwargs)
    #     context['form'] = InventoryForm()
    #     return context
    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            form = TournamentForm(data=self.request.POST)
        else:
            form = TournamentForm()
        # context = super(AddBotView, self).get_context_data()
        # context['form'] = TournamentForm()
        # return context
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
