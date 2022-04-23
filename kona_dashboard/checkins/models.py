from django.db import models


class DailyCheckIn(models.Model):
    SLACK = 1
    PLATFORM = (("Slack", SLACK),)

    RED = 1
    YELLOW = 2
    GREEN = 3
    COLORS = (("Red", RED), ("Yellow", YELLOW), ("Green", GREEN))

    elaboration = models.TextField(blank=True, null=True)
    emotion = models.CharField(null=True, max_length=255)
    platform = models.PositiveIntegerField(choices=PLATFORM, default=1)
    color = models.PositiveIntegerField(choices=COLORS)
    organization = models.CharField("Organization Name", max_length=255)
    team = models.CharField("Team Name", max_length=255)
    username = models.CharField("Username", max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
