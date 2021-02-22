import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkerApp.settings')
app = Celery('WorkerApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Europe/Kiev'


# The task "work_ua_insert" will be started at 11:40 every day
app.conf.beat_schedule = {
    'work_ua_insert_3_am': {
        'task': 'main.tasks.work_ua_insert',
        'schedule': crontab(hour=18, minute=3)
    }
}

# # The task "rabota_ua_insert" will be started at 11:40 every day
# app.conf.beat_schedule = {
#     'rabota_ua_insert_3_am': {
#         'task': 'main.tasks.rabota_ua_insert',
#         'schedule': crontab(hour=21, minute=00)
#     }
# }

# # The task "jooble_insert" will be started at 11:40 every day
# app.conf.beat_schedule = {
#     'jooble_insert_3_am': {
#         'task': 'main.tasks.jooble_insert',
#         'schedule': crontab(hour=19, minute=48)
#     }
# }