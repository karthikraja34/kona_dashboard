from django.contrib import admin

from kona_dashboard.checkins.models import DailyCheckIn, MentalHealthScoreboard


@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    pass


@admin.register(MentalHealthScoreboard)
class MentalHealthScoreboardAdmin(admin.ModelAdmin):
    pass
