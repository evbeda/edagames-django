from django.urls import path
from .views import Home, register
from django.contrib.auth import views as auth_views
from auth_app import views as authr_views


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='auth_app/login.html'),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LoginView.as_view(template_name='auth_app/login.html'),
        name='logout',
    ),
    path('register/', authr_views.register, name='register'),
]
