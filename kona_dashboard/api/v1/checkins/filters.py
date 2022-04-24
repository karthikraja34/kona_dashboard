import django_filters
from django_filters import DateFilter

from kona_dashboard.checkins.models import MentalHealthScoreboard


class ScoreboardFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_from", lookup_expr="gte")
    end_date = DateFilter(field_name="date_from", lookup_expr="lte")

    class Meta:
        model = MentalHealthScoreboard
        fields = ["category", "start_date", "end_date"]
