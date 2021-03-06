from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from .forms import UserRegisterForm


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


class Profile(LoginRequiredMixin, DetailView):
    def get_object(self):
        return self.request.user


class FAQ(LoginRequiredMixin, generic.TemplateView):
    template_name = 'auth_app/faq.html'
