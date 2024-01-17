from django.db import models


class Treatment(models.Model):
    patient = models.ForeignKey("patient.Patient", on_delete=models.PROTECT, related_name="treatments")

    notes = models.TextField(null=True, blank=True)

    date = models.DateField(editable=True, db_index=True)
    dose_mg = models.FloatField()

    infusion_period_minutes = models.IntegerField(null=True)

    stage = models.IntegerField(null=True)

    drug_name = models.CharField(max_length=180, null=True)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["patient", "date"])
        ]
