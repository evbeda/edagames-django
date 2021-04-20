from django.urls import path
from development.views import Challenge
from development.views import MatchListView


app_name = 'development'
urlpatterns = [
    path('challenge', Challenge.as_view(), name='challenge'),
    path('match_history', MatchListView.as_view(), name='match_history'),
]
