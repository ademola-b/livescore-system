from django.db import models

# Create your models here.
tournament_choice = [
    ('rector_cup', 'rector_cup'),
    ('departmental', 'departmental'),
]

class Department(models.Model):
    deptName = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.deptName

class Team(models.Model):
    deptName = models.OneToOneField(Department, on_delete=models.CASCADE)
    coach = models.CharField(max_length=30)

    def __str__(self):
        return self.deptName.deptName

class Tournament(models.Model):
    name = models.CharField(max_length=15, choices=tournament_choice)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    session = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Player(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='upload/', blank=True, null=True)
    age = models.IntegerField()
    jersey_number = models.IntegerField()
    position = models.CharField(max_length=20)
    goals = models.IntegerField()
    assists = models.IntegerField()
    is_captain = models.BooleanField()

    def __str__(self):
        return self.name
    
    
