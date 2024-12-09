import os

from celery import Celery

from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

app = Celery("conf")
app.config_from_object(f"django.conf.settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    "send_email_from_celery_beat": {
        "task": "notifications.tasks.send_sale_email",
        "schedule": crontab(minute="05", hour="18", day_of_week="5"),
    },
}
