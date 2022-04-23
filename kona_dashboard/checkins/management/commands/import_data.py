import csv
from datetime import datetime
from typing import Any

from django.core.management import CommandParser
from django.core.management.base import BaseCommand

from kona_dashboard.checkins.models import DailyCheckIn, Organization, Team
from kona_dashboard.users.models import User


def get_color(color):
    if color.lower() == "yellow":
        return DailyCheckIn.YELLOW
    elif color.lower() == "red":
        return DailyCheckIn.RED
    elif color.lower() == "green":
        return DailyCheckIn.GREEN


class Command(BaseCommand):
    help = "Import bulk daily checkins"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("path", type=str)

    def handle(self, *args: Any, **options: Any):
        DailyCheckIn.objects.all().delete()
        with open(options.get("path")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            checkins = []
            for row_number, row in enumerate(csv_reader):
                if row_number == 0:
                    continue
                organization, _ = Organization.objects.get_or_create(name=row[10])
                team, _ = Team.objects.get_or_create(
                    name=row[11], defaults={"organization": organization}
                )
                user, _ = User.objects.get_or_create(username=row[12])
                checkin = DailyCheckIn(
                    created=datetime.utcfromtimestamp(float(row[1])),
                    elaboration=row[2],
                    emotion=row[3],
                    color=get_color(row[8]),
                    team=team,
                    user=user,
                )
                checkins.append(checkin)

            DailyCheckIn.objects.bulk_create(checkins)
