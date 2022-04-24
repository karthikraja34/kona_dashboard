from datetime import datetime, timedelta

from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from kona_dashboard.api.v1.checkins.filters import ScoreboardFilter
from kona_dashboard.api.v1.checkins.serializers import (
    DailyCheckInSerializer,
    ScoreboardSerializer,
    TeamsSerializer,
)
from kona_dashboard.checkins.models import DailyCheckIn, MentalHealthScoreboard, Team
from kona_dashboard.users.models import User


class ScoreView(ListAPIView):
    serializer_class = ScoreboardSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ScoreboardFilter

    def get_queryset(self):
        queryset = MentalHealthScoreboard.objects.filter().select_related("user")

        if self.request.GET.get("timeline"):
            queryset = MentalHealthScoreboard.objects.for_timeline(
                self.request.GET.get("timeline")
            )

        if self.request.GET.get("team"):
            users = User.objects.filter(teams=self.request.GET["team"])
            return queryset.filter(user__in=users)
        return queryset


class TeamsListView(ListAPIView):
    serializer_class = TeamsSerializer
    queryset = Team.objects.all()


class TrendsListView(ListAPIView):
    serializer_class = DailyCheckInSerializer

    def get_queryset(self):
        past_three_days_checkin_ids = (
            DailyCheckIn.objects.filter(created__gte=datetime.now() - timedelta(days=3))
            .distinct("user")
            .values_list("id", flat=True)
        )
        user_ids = (
            DailyCheckIn.objects.filter(id__in=past_three_days_checkin_ids)
            .values("user")
            .annotate(Avg("health_score"))
            .order_by()
            .filter(health_score__avg__lte=50)
            .values_list("user_id", flat=True)
        )
        return (
            DailyCheckIn.objects.filter(user_id__in=user_ids)
            .order_by("user", "-created")
            .distinct("user")
        )


@api_view(["GET"])
def mental_health_time_analytics_view(request):
    paginator = PageNumberPagination()
    paginator.page_size = 200
    queryset = MentalHealthScoreboard.objects.all()
    _filter = ScoreboardFilter(request.GET, queryset=queryset)
    results = (
        _filter.qs.order_by().values("date_from").annotate(score=100 - Avg("score"))
    )
    paginator.paginate_queryset(results, request)
    return paginator.get_paginated_response(results)
