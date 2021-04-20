from django.urls import path
from development.views import Challenge


app_name = 'development'
urlpatterns = [
    path('challenge', Challenge.as_view(), name='challenge'),
]
