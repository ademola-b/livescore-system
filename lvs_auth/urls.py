from django.urls import path
from . views import (LoginView, DashboardView, 
                     TeamsView, TeamFormView, TeamPlayers, TeamPlayersFormView)


app_name = 'auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('teams/', TeamsView.as_view(), name='team'),
    path('add-team/', TeamFormView.as_view(), name='team_form'),
    path('<int:id>/players/', TeamPlayers.as_view(), name='team_players'),
    path('add-players/', TeamPlayersFormView.as_view(), name='add_players'),
]
