from django.contrib.auth import get_user_model
from rest_framework import serializers

from kona_dashboard.checkins.models import MentalHealthScoreboard, Team

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class ScoreboardSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = MentalHealthScoreboard
        fields = ["user", "category", "score", "date_from"]


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]
