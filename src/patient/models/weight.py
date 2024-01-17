from django.db import models


class WeightLog(models.Model):
    date = models.DateField()
    kilograms = models.IntegerField()
    patient = models.ForeignKey(
        "patient.Patient", on_delete=models.PROTECT, related_name="weight_log"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "kilograms", "patient"],
                name="weight_log_record_unique"
            )
        ]
        indexes = [
            models.Index(fields=["patient", "date"], name="patient_date_index")
        ]
