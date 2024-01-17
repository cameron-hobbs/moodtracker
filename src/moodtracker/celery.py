import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

app = Celery(
    "",
    broker=os.environ.get("BROKER_URL", "amqp://host.docker.internal"),
    broker_transport_options={
        "region": "eu-west-1"
    }
)

app.autodiscover_tasks()

app.conf.update(
    task_default_queue=f"{settings.ENVIRONMENT}_mood_tracker",
    task_serializer="json",
    accept_content=["json"],
    ignore_results=True,
    beat_schedule={
        "batch_sms_notify": {
            "task": "tracker.tasks.batch_sms_notify_schedule",
            "schedule": crontab(hour=12, minute=0)
        }
    }
)

if __name__ == "__main__":
    app.start()
