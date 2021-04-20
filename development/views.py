# from django.views.generic.detail import DetailView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class Challenge(LoginRequiredMixin, generic.TemplateView):
    template_name = 'development/challenge.html'
