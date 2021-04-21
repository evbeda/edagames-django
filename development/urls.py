from django.urls import path
from development.views import ChallengeView
from development.views import MatchListView


app_name = 'development'
urlpatterns = [
    path(
        'challenge',
        ChallengeView.as_view(template_name='development/challenge.html'),
        name='challenge',
    ),
    path(
        'match_history',
        MatchListView.as_view(),
        name='match_history'),
]
