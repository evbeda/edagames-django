from django.urls import path
from development.views import (
    AddBotView,
    ChallengeView,
    delete_bot,
    MatchDetailsView,
    MatchListView,
    MyBotsView,
)
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
        'match_details/<int:pk>',
        MatchDetailsView.as_view(),
        name='match_details',
    ),
    path(
        'mybots',
        MyBotsView.as_view(),
        name='mybots',
    ),
    path(
        'bots/<int:pk>/delete',
        delete_bot,
        name='delete_bot',
    ),
    path('match', views_api.match_list),
    path(
        'addbot',
        AddBotView.as_view(),
        name='addbot',
    ),
]
