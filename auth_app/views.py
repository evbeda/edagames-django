from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    FormView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from .forms import UserRegisterForm
from .models import UserProfile
import requests


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home.html'
    login_url = 'auth:login'


class Registration(FormView):
    template_name = 'auth_app/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class Profile(LoginRequiredMixin, UpdateView):
    fields = [
        'country',
        'region',
        'city_zone',
        'linkedin_profile',
        'github_username',
        'education_background',
        'english_level',
        'intro',
    ]
    success_url = reverse_lazy('auth:home')
    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return UserProfile(
                user=self.request.user,
                country='Argentina',
            )

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        kwargs['user'] = self.request.user
        return super().get_context_data(**kwargs)


class FAQ(LoginRequiredMixin, generic.TemplateView):
    template_name = 'auth_app/faq.html'
