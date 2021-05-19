from django.urls import path
from development.views import ChallengeView
from development.views import MatchListView
from development import views_api


app_name = 'development'
urlpatterns = [
    path(
        'challenge',
        ChallengeView.as_view(),
        name='challenge',
    ),
    path(
        'match_history',
        MatchListView.as_view(),
        name='match_history',
    ),
    path('match', views_api.match_list),
]
