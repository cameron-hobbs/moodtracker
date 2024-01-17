import pytest

from patient.models import Patient
from tracker.models import MoodTracker
from tracker.query.daily_trackers import create_new_trackers


@pytest.mark.django_db
def test_create_daily_trackers(patient_factory):
    patients = patient_factory.create_batch(20)
    create_new_trackers(Patient.objects.all())

    assert MoodTracker.objects.filter(
        patient__in=patients,
        active=True
    ).count() == 20
