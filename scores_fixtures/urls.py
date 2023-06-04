from django.urls import path
from .views import HomeView, HomeViewL, FixturesView, DeleteFixtureView, UpdateFixtureView

app_name = 'scores'
urlpatterns = [
    # path('', HomeView.as_view(), name='index'),
    path('', HomeViewL, name='index'),
    path('fixtures/<str:template_name>/', FixturesView.as_view(), name='fixtures'),
    path('fixtures/<str:template_name>/update/<int:pk>/',UpdateFixtureView.as_view(), name='update_fixture'),
    path('fixtures/<str:template_name>/delete/<int:pk>/', DeleteFixtureView.as_view(), name='delete_fixture'),
    path('matches/<str:template_name>/', FixturesView.as_view(), name='matches'),
]
