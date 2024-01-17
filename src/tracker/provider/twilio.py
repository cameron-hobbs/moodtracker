import os

from twilio.request_validator import RequestValidator
from twilio.rest import Client

from tracker.provider.exceptions import NoLongerSupported


class TwilioWrapper:
    def __init__(self):
        account = os.environ["TWILIO_ACCOUNT_SID"]
        self._token = os.environ["TWILIO_ACCOUNT_TOKEN"]
        self._client = Client(account, self._token)

    def send_bulk_sms(self, patients):
        bindings = [
            "{\"binding_type\":\"sms\",\"address\":\"" + f"{patient.primary_contact_no}" + "\"}"
            for patient in patients.iterator()
        ]

        self._client.notify.services("XX").notifications.create(
            to_binding=bindings,
            body="Copy text"
        )

        raise NoLongerSupported

    def authenticate_webhook_callback(self, request):
        validator = RequestValidator(self._token)

        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.META.get("HTTP_X_TWILIO_SIGNATURE", "")
        )

        return request_valid

    def webhook_callback(self):
        raise NotImplementedError
