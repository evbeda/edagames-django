from django.urls import path
from .views import Home, Registration, Profile, FAQ
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path(
        '',
        Home.as_view(template_name='auth_app/home.html'),
        name='home',
    ),
    path(
        'login/react/',
        TemplateView.as_view(template_name = 'index.html'),
        name='login',
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='auth_app/login.html'),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='auth_app/login.html'),
        name='logout',
    ),
    path('register/', Registration.as_view(), name='register'),

    path('profile/', Profile.as_view(template_name='auth_app/profile.html'), name='profile'),
    path('faq/', FAQ.as_view(template_name='auth_app/faq.html'), name='faq'),
]

