import logging
import os
from datetime import date

from django.db import transaction
from requests import RequestException

from patient.models import Patient
from tracker.provider.sms_provider import SMSProvider
from tracker.query.daily_trackers import create_new_trackers


logger = logging.getLogger("tracker")


class PatientSmsBatchSender:
    _BATCH_SIZE = int(os.environ.get("SMS_BATCH_SIZE", 100))

    def __init__(self):
        self._patients = Patient.objects.none()
        self._sms_provider = SMSProvider()

        self._today = date.today()

    def retrieve_waiting_patients(self):
        patients = Patient.objects.filter_not_sent_sms_since(
            self._today
        )[:self._BATCH_SIZE]

        if not patients.exists():
            logger.info("No patients left with texts needing to be sent")
            return False

        logger.info("Found patients with no text sent for the day")

        self._patients = patients

        return True

    def send_sms(self):
        try:
            self._sms_provider.send_bulk(self._patients)
        except RequestException as e:
            logger.debug("There was a request error for sending bulk sms")
            logger.error(str(e), logging.ERROR)
            return False

        with transaction.atomic():
            Patient.objects.update_last_sms_sent(self._patients, self._today)

            create_new_trackers(self._patients)

        logger.info("Updated db records")

        return True
