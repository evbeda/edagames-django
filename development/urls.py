from django.urls import path
from development.views import ChallengeView
from development.views import MatchListView
from development.views import MyBotsView
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
    path(
        'mybots',
        MyBotsView.as_view(),
        name='mybots',
    ),
    path('match', views_api.match_list),
]
