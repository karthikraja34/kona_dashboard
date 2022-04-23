from django.db import models


class DailyCheckIn(models.Model):
    SLACK = 1
    PLATFORM = (("Slack", SLACK),)

    RED = 1
    YELLOW = 2
    GREEN = 3
    COLORS = ((RED, "Red"), (YELLOW, "Yellow"), (GREEN, "Green"))

    elaboration = models.TextField(blank=True, null=True)
    emotion = models.CharField(null=True, max_length=255)
    platform = models.PositiveIntegerField(choices=PLATFORM, default=1)
    color = models.PositiveIntegerField(choices=COLORS)
    team = models.ForeignKey("checkins.Team", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " is feeling " + self.get_color_display()


class Team(models.Model):
    name = models.CharField(max_length=1024)
    organization = models.ForeignKey("checkins.Organization", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
