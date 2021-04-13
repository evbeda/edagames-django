from django.shortcuts import render, redirect
from django.views import generic
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_in
from .signals import show_token


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home.html'
    login_url = 'login'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Your account has been created for {username}! Log in now',
            )
            return redirect('auth:login')
    else:
        form = UserRegisterForm()
    return render(request, 'auth_app/register.html', {'form': form})


user_logged_in.connect(show_token)
