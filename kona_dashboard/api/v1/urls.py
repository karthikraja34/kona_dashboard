from django.urls import path

from .checkins.views import (
    ScoreView,
    TeamsListView,
    TrendsListView,
    mental_health_time_analytics_view,
)

urlpatterns = [
    path("scores/", ScoreView.as_view()),
    path("teams/", TeamsListView.as_view()),
    path("trends/", TrendsListView.as_view()),
    path("score_analytics/", mental_health_time_analytics_view),
]
