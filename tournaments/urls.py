from django.urls import (
    path,
)
from .views import (
    CreateTournamentView,
    PendingTournamentListView,
    RegistrationTournamentView,
    TournamentGeneratorView,
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
        'tournament_generator/',
        TournamentGeneratorView.as_view(),
        name='tournament_generator',
    ),
    path(
        'tournaments_history/',
        TournamentListView.as_view(),
        name='tournaments_history',
    ),
    path(
        'tournaments_pending/',
        PendingTournamentListView.as_view(),
        name='tournaments_pending',
    ),
    path(
        'tournament_results/<int:pk>/',
        TournamentResultsView.as_view(),
        name='tournament_results',
    ),
    path(
        'tournament_registration/',
        RegistrationTournamentView.as_view(),
        name='tournament_registration',
    ),
]
