from django.db import models

from tournament.models import Tournament, Team
# Create your models here.
class Fixture(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.CASCADE)
    match_date_time = models.DateTimeField()

    def __str__(self):
        return "{0} vs {1}".format(self.home_team, self.away_team)

class Match(models.Model):
    fixture = models.OneToOneField(Fixture, on_delete=models.CASCADE)
    home_team_score = models.CharField(max_length=10, default=0, blank=True, null=True,)
    away_team_score = models.CharField(max_length=10, default=0, blank=True, null=True,)
    home_team_formation = models.CharField(max_length=10)
    away_team_formation = models.CharField(max_length=10)
    referee = models.CharField(max_length=30)
    
    def __str__(self):
        return "{0} vs {1}".format(self.home_team, self.away_team)

class GoalScorers(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    home_scorer = models.ForeignKey(Team, related_name='home_scorer', blank=True, null=True, on_delete=models.CASCADE)
    away_scorer = models.ForeignKey(Team, related_name='away_scorer', blank=True, null=True, on_delete=models.CASCADE)
    home_assist = models.ForeignKey(Team, related_name='home_assist', blank=True, null=True, on_delete=models.CASCADE)
    away_assist = models.ForeignKey(Team, related_name='away_assist', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Goal Scorers"
    def __str__(self):
        return self.match
    


