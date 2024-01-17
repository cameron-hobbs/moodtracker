import base64
import logging
import os

import requests
from django.utils import timezone

from patient.models import Patient
from tracker.models import MoodTracker


logger = logging.getLogger("tracker")


class TxtLocalWrapper:
    _BASE_URL = "https://api.txtlocal.com/"

    def send_bulk_sms(self, patients):
        api_key = os.environ['TXT_LOCAL_API_KEY']

        numbers = ",".join(list(patients.values_list("primary_contact_no", flat=True)))

        message = "Please reply with your current mood on a scale of 1-10. " \
                  "Where 1 is the lowest and 10 is the highest."

        data = {
            "message": message,
            "numbers": numbers,
            "apikey": api_key,
            "test": os.environ.get("TEST_SMS", "True").lower() == "true"
        }

        logger.info("Sending bulk sms request")
        logger.info(data)

        res = requests.post(self._BASE_URL + "send/?", data=data)
        res.raise_for_status()

        logger.info(res.status_code)
        logger.info(res.json())

        logger.info("Sent bulk sms request")

        return res

    @classmethod
    def authenticate_webhook_callback(cls, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            logger.info("No auth data, could not verify callback")
            return False

        auth = request.META['HTTP_AUTHORIZATION'].split()

        if len(auth) != 2:
            logger.info("No username and pass for auth")
            return False

        if auth[0].lower() != "basic":
            logger.info("Must be basic auth")
            return False

        username, password = base64.b64decode(auth[1]).decode("utf-8").split(':')

        return str(username) == os.environ.get(
            "WEBHOOK_USERNAME", "moodtracker"
        ) and password == os.environ["WEBHOOK_PASS"]

    @staticmethod
    def webhook_callback(request):
        try:
            phone_number = "+" + request.data["sender"].strip()
            message = request.data["content"].strip()
        except KeyError:
            logger.info("Could not find phone number/content in callback")
            return False

        mood = int(message)

        try:
            patient = Patient.objects.get(primary_contact_no=phone_number)
        except Patient.DoesNotExist:
            logger.info("Could not find patient with phone number")
            return False
        else:
            logger.info("Found patient with phone number")

        tracker = MoodTracker.objects.filter(patient=patient).order_by("-date").first()

        if tracker is None:
            logger.info("Could not find recent mood tracker record")
            return False

        logger.info("Found recent mood tracker record")

        tracker.mood_score = mood
        tracker.sms_received = timezone.now()
        tracker.active = False
        tracker.save()

        return True
