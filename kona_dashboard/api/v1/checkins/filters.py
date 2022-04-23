import django_filters

from kona_dashboard.checkins.models import MentalHealthScoreboard


class ScoreboardFilter(django_filters.FilterSet):
    class Meta:
        model = MentalHealthScoreboard
        fields = ["category"]
