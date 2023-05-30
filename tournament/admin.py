from django.contrib import admin
from . models import *
# Register your models here.

admin_models = [
    Department, Team, Tournament, Player
]

for model in admin_models:
    admin.site.register(model)