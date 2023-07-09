from django.urls import path
from . views import (LoginView, DashboardView,TeamsView, 
                     TeamPlayers, DeleteTeam, UpdateMatchScoreV, UpdateTeam, 
                      DeletePlayer, UpdatePlayer, 
                      UpdateMatch)


app_name = 'auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('teams/', TeamsView.as_view(), name='team'),
    path('teams/<str:pk>/update/', UpdateTeam.as_view(), name='update_team'),
    path('teams/<str:pk>/delete/', DeleteTeam.as_view(), name='delete_team'),
    # path('add-team/', TeamFormView.as_view(), name='team_form'),
    path('<str:pk>/players/', TeamPlayers.as_view(), name='team_players'),
    # path('players/<int:pk>/update/', updatePlayer(), name='update_player'),
    path('players/<int:pk>/update/', UpdatePlayer.as_view(), name='update_player'),
    path('players/<int:pk>/delete/', DeletePlayer.as_view(), name='delete_player'),

    path('match/<int:pk>/update/', UpdateMatch.as_view(), name="update_match"),
    path('score/<int:pk>/update/', UpdateMatchScoreV.as_view(), name="update_match_score")
]
