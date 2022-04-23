from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from kona_dashboard.api.v1.checkins.filters import ScoreboardFilter
from kona_dashboard.api.v1.checkins.serializers import (
    ScoreboardSerializer,
    TeamsSerializer,
)
from kona_dashboard.checkins.models import MentalHealthScoreboard, Team
from kona_dashboard.users.models import User


class ScoreView(ListAPIView):
    serializer_class = ScoreboardSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ScoreboardFilter

    def get_queryset(self):
        if self.request.GET.get("team"):
            users = User.objects.filter(teams=self.request.GET["team"])
            return MentalHealthScoreboard.objects.filter(user__in=users).select_related(
                "user"
            )
        return MentalHealthScoreboard.objects.all().select_related("user")


class TeamsListView(ListAPIView):
    serializer_class = TeamsSerializer
    queryset = Team.objects.all()
