from django.core.validators import RegexValidator
from django.db import models

from patient.repository import PatientRepository


class Gender(models.TextChoices):
    MALE = "male"
    FEMALE = "female"


_PHONE_REGEX = RegexValidator(
    regex=r'^\+((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|'
          r'9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\W*\d){0,13}\d$',
    message="Phone number must be entered international format starting with +"
)


class PatientSupport(models.Model):
    name = models.CharField(max_length=180, null=True, blank=True)
    primary_contact_no = models.CharField(validators=[_PHONE_REGEX], max_length=50, null=True, blank=True)
    secondary_contact_no = models.CharField(validators=[_PHONE_REGEX], max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=180, null=True, blank=True)
    address = models.CharField(max_length=2000, null=True, blank=True)


class Patient(models.Model):
    primary_diagnosis = models.CharField(max_length=180)
    primary_contact_no = models.CharField(validators=[_PHONE_REGEX], max_length=50, unique=True)

    receive_mood_tracker_sms = models.BooleanField(default=True)

    last_sms_sent = models.DateField(null=True)

    date_of_birth = models.DateField(null=True)
    sex = models.CharField(choices=Gender.choices, max_length=10, null=True, blank=True)
    secondary_contact_no = models.CharField(validators=[_PHONE_REGEX], max_length=50, null=True, blank=True)
    address = models.CharField(max_length=2000, null=True, blank=True)
    occupation = models.CharField(max_length=180, null=True, blank=True)

    next_of_kin = models.OneToOneField(
        PatientSupport, on_delete=models.PROTECT, related_name="next_of_kin", null=True
    )

    gp = models.OneToOneField(
        PatientSupport, on_delete=models.PROTECT, related_name="gp", null=True
    )

    physciatrist = models.OneToOneField(
        PatientSupport, on_delete=models.PROTECT, related_name="physciatrist", null=True
    )

    allergies = models.CharField(max_length=2000, null=True, blank=True)
    current_medication = models.CharField(max_length=180, null=True, blank=True)
    other_notes = models.CharField(max_length=2000, null=True, blank=True)

    objects = PatientRepository.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["receive_mood_tracker_sms", "last_sms_sent"])
        ]
