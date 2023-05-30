from django.urls import path
from . views import RectorCupView

app_name = 'tournament'
urlpatterns = [
    path('rector-cup/', RectorCupView.as_view(), name="rector_cup")
]
