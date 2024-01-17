from unittest.mock import MagicMock

import pytest

from patient.models import Patient
from tracker.models import MoodTracker
from tracker.sms_sender import PatientSmsBatchSender


@pytest.mark.django_db
def test_retrieve_waiting_patients_none():
    assert not PatientSmsBatchSender().retrieve_waiting_patients()


@pytest.mark.django_db
def test_retrieve_waiting_patients(patient_factory):
    patient_factory.create_batch(
        10, last_sms_sent=None, receive_mood_tracker_sms=True
    )

    batch_sender = PatientSmsBatchSender()

    assert batch_sender.retrieve_waiting_patients()

    assert [patient.id for patient in batch_sender._patients] == list(
        Patient.objects.values_list("id", flat=True)
    )


@pytest.mark.django_db
def test_send_sms_patients(patient_factory):
    patient_factory.create_batch(
        10, last_sms_sent=None, receive_mood_tracker_sms=True
    )

    batch_sender = PatientSmsBatchSender()
    batch_sender.retrieve_waiting_patients()

    batch_sender._sms_provider.send_bulk = MagicMock()

    batch_sender.send_sms()

    assert batch_sender._sms_provider.send_bulk.call_count == 1

    assert [
        patient.last_sms_sent == batch_sender._today
        for patient in batch_sender._patients
    ]

    assert MoodTracker.objects.count() == batch_sender._patients.count()
