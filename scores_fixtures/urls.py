from django.urls import path
from .views import HomeView, FixturesView

app_name = 'scores'
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('fixtures/<str:template_name>/', FixturesView.as_view(), name='fixtures'),
    path('fixtures/departmental-fixtures/', FixturesView.as_view(), name='departmental_fixtures'),
]
