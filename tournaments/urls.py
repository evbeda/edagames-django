from django.urls import path
from .views import CreateTournamentView
from .views import TournamentResult


app_name = 'tournaments'
urlpatterns = [
    path(
        'create_tournament',
        CreateTournamentView.as_view(),
        name='create_tournament',
    ),
    path(
        'tournament_results',
        TournamentResult.as_view(),
        name='results',
    ),
]
