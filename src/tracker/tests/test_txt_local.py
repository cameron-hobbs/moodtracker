import pytest

from patient.models import Patient
from tracker.provider.txtlocal import TxtLocalWrapper


def test_base_url():
    assert TxtLocalWrapper._BASE_URL == "https://api.txtlocal.com/"


@pytest.mark.django_db
def test_send_bulk_sms(requests_mock, monkeypatch, patient_factory):
    monkeypatch.setenv("TXT_LOCAL_API_KEY", "fake_key")
    monkeypatch.setenv("TEST_SMS", "True")
    patient_factory.create_batch(5)

    adapter = requests_mock.post(TxtLocalWrapper._BASE_URL + "send/?")

    assert TxtLocalWrapper().send_bulk_sms(Patient.objects.all())

    assert adapter.call_count == 1


def test_authenticate_webhook_callback():
    assert False
