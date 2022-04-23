# Generated by Django 3.2.13 on 2022-04-23 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checkins', '0002_auto_20220423_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailycheckin',
            name='health_score',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='MentalHealthScoreboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('score', models.IntegerField(default=0)),
                ('category', models.PositiveIntegerField(choices=[(1, 'Daily Score'), (2, 'Weekly Score'), (3, 'Monthly Score')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('checkins', models.ManyToManyField(related_name='checkin_stats', to='checkins.DailyCheckIn')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mental_scores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-score', '-date_from'),
                'unique_together': {('user', 'date_from', 'category')},
            },
        ),
    ]
