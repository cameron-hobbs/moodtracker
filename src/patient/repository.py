from django.contrib.auth.models import UserManager
from django.db.models import QuerySet, Q


class CustomUserQueryset(QuerySet):
    def preload_patient(self):
        return self.select_related(
            "patient__next_of_kin", "patient__gp", "patient__physciatrist"
        ).prefetch_related("patient__weight_log")


class CustomUserRepository(UserManager):
    def get_queryset(self):
        return CustomUserQueryset(model=self.model, using=self._db, hints=self._hints)


class PatientRepository(QuerySet):
    def filter_not_sent_sms_since(self, date):
        last_sent_sms_not_today = Q(
            receive_mood_tracker_sms=True, last_sms_sent__lt=date
        )
        never_sent_sms = Q(receive_mood_tracker_sms=True, last_sms_sent__isnull=True)

        return self.filter(
            last_sent_sms_not_today | never_sent_sms
        )

    def update_last_sms_sent(self, patients, date):
        # For updating a slice of patients
        return self.filter(
            id__in=[patient.id for patient in patients]
        ).update(last_sms_sent=date)
