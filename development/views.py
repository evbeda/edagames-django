# from django.views.generic.detail import DetailView
from django.views import generic
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Match


class Challenge(LoginRequiredMixin, generic.TemplateView):
    template_name = 'development/challenge.html'


class MatchListView(ListView):
    template_name = 'development/match_history.html'
    model = Match
