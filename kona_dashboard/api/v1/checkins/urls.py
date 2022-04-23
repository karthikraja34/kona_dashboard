from django.urls import path

from . import views

urlpatterns = [
    path("scores/", views.ScoreView.as_view()),
    path("teams/", views.TeamsListView.as_view()),
]
