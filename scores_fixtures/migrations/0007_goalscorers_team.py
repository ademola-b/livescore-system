# Generated by Django 4.2.1 on 2023-06-04 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
        ('scores_fixtures', '0006_rename_home_assist_goalscorers_assist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalscorers',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tournament.team'),
        ),
    ]
