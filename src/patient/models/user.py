from django.contrib.auth.models import AbstractUser
from django.db import models

from patient.repository import CustomUserRepository


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180)
    patient = models.OneToOneField("patient.Patient", null=True, on_delete=models.CASCADE)

    clinician = models.ForeignKey(
        "patient.CustomUser", null=True, related_name="clients", on_delete=models.PROTECT
    )

    objects = CustomUserRepository()

    def get_patients(self):
        return self.clients.select_related("patient")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["patient", "clinician"], name="patient_clinician_unique")
        ]
