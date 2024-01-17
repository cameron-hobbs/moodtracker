import logging

from django.core.cache import cache
from moodtracker.celery import app
from tracker.sms_sender import PatientSmsBatchSender
from tracker.task_locking import acquire_lock_blocking

logger = logging.getLogger("tracker")


@app.task(acks_late=True)
def batch_sms_notify_schedule():
    logger.info("Beat started")

    batch_sms_notify.delay()


@app.task(bind=True, acks_late=True, max_retries=5, soft_time_limit=60)
def batch_sms_notify(self):
    logger.info("Batch sms notify task started")

    cache_key = "batch_sms_notify"

    acquire_lock_blocking(cache_key)

    batch_sender = PatientSmsBatchSender()

    if not batch_sender.retrieve_waiting_patients():
        return

    sent_sms = batch_sender.send_sms()

    cache.delete(cache_key)

    if not sent_sms:
        self.retry(countdown=3)
        return

    batch_sms_notify.delay()

    logger.info("We go again...")
