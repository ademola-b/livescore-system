# Generated by Django 4.2.1 on 2023-07-08 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
        ('scores_fixtures', '0014_goalscorers_away_score_goalscorers_home_score_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scores_fixtures.match')),
                ('red_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='red_card', to='tournament.player')),
                ('yellow_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='yellow_card', to='tournament.player')),
            ],
        ),
    ]
