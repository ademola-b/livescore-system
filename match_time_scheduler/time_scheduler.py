from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from lvs_auth.views import UpdateMatch

from scores_fixtures.models import Match

scheduler = BackgroundScheduler()

def match_time():
        match = Match.objects.get(fixture__match_date_time__date=date.today())
        global scheduler
        if match.status == 'ON':
            match.time += 1
            print(f"time: {match.time}")
            match.save()
        elif match.status == 'FT':
            scheduler.remove_job('time_0001')
        elif match.status == 'HT':
            scheduler.pause_job('time_0001')

def start():
    # match_time = UpdateMatch()
    global scheduler
    scheduler.add_job(
        match_time, 
        "interval", minutes = 0.5,
        id="time_0001", replace_existing=True)
    
    scheduler.start()
