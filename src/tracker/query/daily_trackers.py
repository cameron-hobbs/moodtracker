from tracker.models import MoodTracker


def create_new_trackers(patients):
    new_trackers = [
        MoodTracker(patient=patient, active=True)
        for patient in patients
    ]

    MoodTracker.objects.bulk_create(new_trackers)
