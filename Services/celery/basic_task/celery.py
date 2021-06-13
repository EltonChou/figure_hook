from celery import Celery
from celery.schedules import crontab

app = Celery("celery", include=("basic_task.tasks"))

app.config_from_object("basic_task.celeryconfig")

app.conf.beat_schedule = {
    'check_new_release': {
        'task': 'basic_task.tasks.check_new_release',
        'schedule': crontab(minute="15, 35, 55"),
    },
    'publish_new_releases_every_10m':  {
        'task': 'basic_task.tasks.news_push',
        'schedule': crontab(minute="*/10"),
    },
}
