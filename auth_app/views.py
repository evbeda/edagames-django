from django.shortcuts import render, redirect
from django.views import generic
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class Home(generic.TemplateView):
    template_name = 'home.html'


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
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
