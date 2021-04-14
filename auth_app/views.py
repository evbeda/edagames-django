from django.views import generic
from .forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_in
from .signals import show_token
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


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


user_logged_in.connect(show_token)
