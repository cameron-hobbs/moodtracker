from unittest.mock import MagicMock

from tracker.provider.sms_provider import SMSProvider
from tracker.provider.txtlocal import TxtLocalWrapper


def test_txt_local_provider(monkeypatch):
    monkeypatch.setenv("TXT_LOCAL_API_KEY", "blah")
    sms_provider = SMSProvider()
    assert isinstance(sms_provider._provider, TxtLocalWrapper)


def test_provider_send_bulk(monkeypatch):
    monkeypatch.setenv("TXT_LOCAL_API_KEY", "blah")
    sms_provider = SMSProvider()
    sms_provider._provider.send_bulk_sms = MagicMock()

    sms_provider.send_bulk([])

    assert sms_provider._provider.send_bulk_sms.call_count == 1


def test_provider_webhook_callback(monkeypatch):
    monkeypatch.setenv("TXT_LOCAL_API_KEY", "blah")
    sms_provider = SMSProvider()

    sms_provider._provider.authenticate_webhook_callback = MagicMock(return_value=True)
    sms_provider._provider.webhook_callback = MagicMock()

    sms_provider.webhook_callback(None)

    assert sms_provider._provider.authenticate_webhook_callback.call_count == 1
    assert sms_provider._provider.webhook_callback.call_count == 1
