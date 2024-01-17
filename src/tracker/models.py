from django.db import models


class MoodTracker(models.Model):
    patient = models.ForeignKey(
        "patient.Patient", on_delete=models.PROTECT, related_name="mood_tracker_scores"
    )
    mood_score = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    sms_received = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["patient", "date"], name="mood_patient_date_index"),
            models.Index(fields=["patient", "date", "active"], name="active_tracker"),
            models.Index(fields=["date", "active"], name="date_active")
        ]
