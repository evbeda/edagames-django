from django.urls import path
from .views import (
    CreateTournamentView,
    TournamentResultsView,
    TournamentListView,
)


app_name = 'tournaments'
urlpatterns = [
    path(
        'create_tournament/',
        CreateTournamentView.as_view(),
        name='create_tournament',
    ),
    path(
        'tournaments_history/',
        TournamentListView.as_view(),
        name='tournaments_history',
    ),
    path(
        'tournament_results/<int:pk>/',
        TournamentResultsView.as_view(),
        name='tournament_results',
    ),
]
