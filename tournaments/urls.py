from django.urls import path
from .views import AddBotView


app_name = 'tournaments'
urlpatterns = [
    path(
        'tournament',
        AddBotView.as_view(),
        name='tournament',
    ),
]
