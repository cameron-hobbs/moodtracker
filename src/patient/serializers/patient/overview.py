from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from patient.models import CustomUser


class PatientOverviewSerializer(ModelSerializer):
    patient_id = SerializerMethodField()
    primary_diagnosis = SerializerMethodField()

    last_treatment = SerializerMethodField()
    last_score = SerializerMethodField()
    change = SerializerMethodField()
    last_recorded = SerializerMethodField()
    seven_day_average = SerializerMethodField()

    def get_patient_id(self, instance):
        return instance.patient.id

    def get_primary_diagnosis(self, instance):
        return instance.patient.primary_diagnosis

    def get_last_treatment(self, instance):
        last_treatment = instance.patient.treatments.last()

        return None if last_treatment is None else last_treatment.date

    def get_last_score(self, instance):
        queryset = instance.patient.mood_tracker_scores.filter(mood_score__isnull=False)
        last_score = queryset.last()

        return None if last_score is None else last_score.mood_score

    def get_change(self, instance):
        queryset = instance.patient.mood_tracker_scores.filter(mood_score__isnull=False)
        last_index = queryset.count()

        if last_index <= 1:
            return None

        last_score = queryset.last().mood_score
        previous_last_score = queryset[last_index - 2].mood_score

        return last_score - previous_last_score

    def get_last_recorded(self, instance):
        last_score = instance.patient.mood_tracker_scores.filter(
            mood_score__isnull=False
        ).last()

        return None if last_score is None else last_score.date

    # This calculation needs to change to be the actual last 7 days, not last 7 mood scores
    def get_seven_day_average(self, instance):
        queryset = instance.patient.mood_tracker_scores.filter(mood_score__isnull=False)
        last_index = queryset.count()

        if last_index <= 6:
            return None

        trackers = queryset[last_index - 7: last_index - 1]

        scores = list(trackers.values_list("mood_score", flat=True))

        return sum(scores) / 7

    class Meta:
        model = CustomUser
        fields = [
            "patient_id",
            "first_name",
            "last_name",
            "primary_diagnosis",
            "last_treatment",
            "last_score",
            "change",
            "last_recorded",
            "seven_day_average"
        ]
        read_only_fields = [
            "patient_id",
            "name",
            "primary_diagnosis",
            "last_treatment",
            "last_score",
            "change",
            "last_recorded",
            "seven_day_average"
        ]
