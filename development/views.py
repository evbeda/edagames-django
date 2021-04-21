from django.views.generic.edit import FormView
from development.forms import ChallengeForm
from django.views.generic.list import ListView
from .models import Match
from django.urls import reverse_lazy


class ChallengeView(FormView):
    form_class = ChallengeForm
    success_url = reverse_lazy('development:challenge')

    def form_valid(self, form):
        return super().form_valid(form)


class MatchListView(ListView):
    template_name = 'development/match_history.html'
    model = Match
