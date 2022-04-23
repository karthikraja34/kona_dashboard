from django.urls import path

from .checkins.views import ScoreView, TeamsListView

urlpatterns = [
    path("scores/", ScoreView.as_view()),
    path("teams/", TeamsListView.as_view()),
]
