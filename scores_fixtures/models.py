from django.db import models

from tournament.models import Tournament, Team, Player
# Create your models here.

match_status = [
    ("not_started", "not_started"),
    ("ON", "ON"),
    ("HT", "HT"),
    ("FT", "FT"),
    ("ET", "ET"),
    ("postponed", "postponed"),
]

class Fixture(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.CASCADE)
    match_date_time = models.DateTimeField()

    def __str__(self):
        return "{0} vs {1}".format(self.home_team, self.away_team)

class Match(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    home_team_score = models.IntegerField(default=0, blank=True, null=True,)
    away_team_score = models.IntegerField(default=0, blank=True, null=True,)
    home_team_formation = models.CharField(max_length=10, default="4-4-2")
    away_team_formation = models.CharField(max_length=10, default="4-4-2")
    referee = models.CharField(max_length=30)
    status = models.CharField(max_length=15, choices=match_status, default="not_started")
    time = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Matches"
    def __str__(self):
        return "{0} vs {1}".format(self.fixture.home_team, self.fixture.away_team)

class GoalScorers(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    scorer = models.ForeignKey(Player, related_name='home_scorer', blank=True, null=True, on_delete=models.CASCADE)
    assist = models.ForeignKey(Player, related_name='home_assist', blank=True, null=True, on_delete=models.CASCADE)
    home_score = models.IntegerField(default=0, null=True, blank=True)
    away_score = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Goal Scorers"
    def __str__(self):
        return f"""Match: {self.match.fixture.home_team.deptName.deptName} - {self.match.fixture.away_team.deptName.deptName}
                    """
    
class Card(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    red_card = models.ForeignKey(Player, related_name='red_card', on_delete=models.CASCADE, null=True, blank=True)
    yellow_card = models.ForeignKey(Player, related_name='yellow_card', on_delete=models.CASCADE, null=True, blank=True)

class MatchStats(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home_corner = models.IntegerField(default=0)
    away_corner = models.IntegerField(default=0)
    home_fouls = models.IntegerField(default=0)
    away_fouls = models.IntegerField(default=0)
    home_ball_possession = models.IntegerField(default=0)
    away_ball_possession = models.IntegerField(default=0)
    home_offside = models.IntegerField(default=0)
    away_offside = models.IntegerField(default=0)

class MatchAdditionalInfo(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    additional_info = models.CharField(max_length=1000, null=True, blank=True)

    



    


