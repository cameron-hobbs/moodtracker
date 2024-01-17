import logging

from tracker.provider.twilio import TwilioWrapper
from tracker.provider.txtlocal import TxtLocalWrapper
import os

logger = logging.getLogger("tracker")


class SMSProvider:
    PROVIDER = os.environ.get("SMS_PROVIDER_IMPL", "txtlocal")

    def __init__(self):
        if self.PROVIDER == "txtlocal":
            self._provider = TxtLocalWrapper()
        elif self.PROVIDER == "twilio":
            self._provider = TwilioWrapper()
        else:
            raise NotImplementedError

    def send_bulk(self, patients):
        return self._provider.send_bulk_sms(patients)

    def _authenticate_webhook_callback(self, request):
        return self._provider.authenticate_webhook_callback(request)

    def webhook_callback(self, request):
        if not self._authenticate_webhook_callback(request):
            logger.info("Could not authenticate webhook callback")
            return

        return self._provider.webhook_callback(request)
