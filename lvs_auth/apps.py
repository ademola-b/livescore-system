from django.apps import AppConfig


class LvsAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lvs_auth'

    # when the application is ready
    def ready(self):
        print("Match about to start")
        from match_time_scheduler import time_scheduler
        time_scheduler.start()
