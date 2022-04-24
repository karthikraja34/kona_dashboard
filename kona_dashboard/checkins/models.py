from datetime import date, timedelta

from django.db import models
from django.utils import timezone
from django.utils.timezone import now

from kona_dashboard.users.models import User


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
    health_score = models.IntegerField(default=0)

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


class ScoreboardDateHelperMixin(object):
    def this_week_start_date(self):
        return timezone.localtime(now()).date() - timedelta(
            days=(timezone.localtime(now()).date().weekday()) % 7
        )

    def this_month_start_date(self):
        return date(
            timezone.localtime(now()).date().year,
            timezone.localtime(now()).date().month,
            1,
        )

    def today(self):
        return timezone.localtime(now()).date(), MentalHealthScoreboard.DAILY_SCORE

    def yesterday(self):
        return (
            timezone.localtime(now()).date() - timedelta(days=1),
            MentalHealthScoreboard.DAILY_SCORE,
        )

    def last_week(self):
        return (
            self.this_week_start_date() - timedelta(days=7),
            MentalHealthScoreboard.WEEKLY_SCORE,
        )

    def last_month(self):
        last_month_end_date = self.this_month_start_date() - timedelta(days=1)
        date_from = date(last_month_end_date.year, last_month_end_date.month, 1)

        return date_from, MentalHealthScoreboard.MONTHLY_SCORE


class MentalHealthScoreboardManager(ScoreboardDateHelperMixin, models.Manager):
    YESTERDAY = "yesterday"
    LAST_MONTH = "last_month"
    LAST_WEEK = "last_week"
    THIS_MONTH = "this_month"
    THIS_WEEK = "this_week"
    TODAY = "today"

    def for_timeline(self, timeline=TODAY):
        if timeline == self.LAST_WEEK:
            date_from, category = self.last_week()
        elif timeline == self.LAST_MONTH:
            date_from, category = self.last_month()
        elif timeline == self.YESTERDAY:
            date_from, category = self.yesterday()
        elif timeline == self.THIS_WEEK:
            date_from = self.this_week_start_date()
            category = MentalHealthScoreboard.WEEKLY_SCORE
        elif timeline == self.THIS_MONTH:
            date_from = self.this_month_start_date()
            category = MentalHealthScoreboard.MONTHLY_SCORE
        else:
            date_from, category = self.today()

        return MentalHealthScoreboard.objects.filter(
            date_from=date_from, category=category
        )

    def update_daily(self, checkin):
        date_from, category = checkin.created.date(), MentalHealthScoreboard.DAILY_SCORE
        scoreboard, created = self.get_or_create(
            date_from=date_from, user=checkin.user, category=category
        )

        if scoreboard.checkins.filter(
            checkin_stats__checkins__created=checkin.created,
            checkin_stats__checkins__user=checkin.user,
        ).exists():
            return
        scoreboard.add_checkin(checkin)

    def update_weekly(self, checkin):
        this_week_start_date = checkin.created.date() - timedelta(
            days=(checkin.created.date().weekday()) % 7
        )
        scoreboard, created = self.get_or_create(
            date_from=this_week_start_date,
            user=checkin.user,
            category=MentalHealthScoreboard.WEEKLY_SCORE,
        )

        if scoreboard.checkins.filter(
            checkin_stats__checkins__created=checkin.created,
            checkin_stats__checkins__user=checkin.user,
        ).exists():
            return
        scoreboard.add_checkin(checkin)

    def update_monthly(self, checkin):
        this_month_start_date = date(
            checkin.created.date().year,
            checkin.created.date().month,
            1,
        )
        scoreboard, created = self.get_or_create(
            date_from=this_month_start_date,
            user=checkin.user,
            category=MentalHealthScoreboard.MONTHLY_SCORE,
        )

        if scoreboard.checkins.filter(
            checkin_stats__checkins__created=checkin.created,
            checkin_stats__checkins__user=checkin.user,
        ).exists():
            return
        scoreboard.add_checkin(checkin)

    def add_checkin(self, checkin):
        self.update_daily(checkin)
        self.update_weekly(checkin)
        self.update_monthly(checkin)


class MentalHealthScoreboard(models.Model):
    DAILY_SCORE = 1
    WEEKLY_SCORE = 2
    MONTHLY_SCORE = 3

    CATEGORIES = (
        (DAILY_SCORE, "Daily Score"),
        (WEEKLY_SCORE, "Weekly Score"),
        (MONTHLY_SCORE, "Monthly Score"),
    )
    user = models.ForeignKey(
        User, related_name="mental_scores", on_delete=models.CASCADE
    )
    date_from = models.DateField()
    score = models.IntegerField(default=0)
    checkins = models.ManyToManyField(DailyCheckIn, related_name="checkin_stats")
    category = models.PositiveIntegerField(choices=CATEGORIES, default=DAILY_SCORE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    objects = MentalHealthScoreboardManager()

    class Meta:
        ordering = ("-score", "-date_from")
        unique_together = (("user", "date_from", "category"),)

    def add_checkin(self, checkin):
        self.checkins.add(checkin)
        self.score = self.checkins.aggregate(models.Avg("health_score"))[
            "health_score__avg"
        ]
        self.save()
