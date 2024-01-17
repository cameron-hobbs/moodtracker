from datetime import date

import pytest
from rest_framework import status
from rest_framework.test import RequestsClient


@pytest.mark.django_db(transaction=True)
def test_sms_webhook_txt_local(
    api_client, monkeypatch, patient_factory, mood_tracker_factory
):
    monkeypatch.setenv("SMS_PROVIDER_IMPL", "txtlocal")
    monkeypatch.setenv("WEBHOOK_PASS", "hello_there")

    data = {
        "sender": "447775230895",
        "content": "8"
    }

    patient = patient_factory(primary_contact_no="+447775230895")

    tracker = mood_tracker_factory(date=date.today(), patient=patient)

    res = RequestsClient().post(
        "http://moodtracker:hello_there@localhost:8000/api/sms_webhook/",
        data=data
    )

    tracker.refresh_from_db()
    assert tracker.mood_score == int(data["content"])

    assert res.status_code == status.HTTP_200_OK
