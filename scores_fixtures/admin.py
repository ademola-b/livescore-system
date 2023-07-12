from django.contrib import admin
from . models import *
# Register your models here.
admin_models = [
    Fixture, Match, GoalScorers, Card, MatchStats, MatchAdditionalInfo
]

for model in admin_models:
    admin.site.register(model)