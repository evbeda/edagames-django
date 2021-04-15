from django.urls import path
from .views import Home, Registration, Profile
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', Home.as_view(), name='home'),
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
    path('profile/<pk>', Profile.as_view(template_name='auth_app/profile.html'), name='profile'),
]
