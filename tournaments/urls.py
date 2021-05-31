from django.urls import path
from .views import CreateTournamentView


app_name = 'tournaments'
urlpatterns = [
    path(
        'create_tournament',
        CreateTournamentView.as_view(),
        name='create_tournament',
    ),
]
