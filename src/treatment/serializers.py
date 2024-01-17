from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from patient.models import Patient
from treatment.models import Treatment


class TreatmentPartialUpdateSerializer(ModelSerializer):
    class Meta:
        model = Treatment
        fields = ("notes", "date", "infusion_period_minutes", "dose_mg", "stage")


class TreatmentSerializer(ModelSerializer):
    days_since = SerializerMethodField()

    treatment_no = SerializerMethodField()

    mg_per_kg = SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(TreatmentSerializer, self).__init__(*args, **kwargs)
        self._queryset = self.context["view"].get_queryset()

    def get_days_since(self, instance):
        for i, treatment in (enumerate(self._queryset)):
            if treatment.id != instance.id:
                continue

            if i == len(self._queryset) - 1:
                return None

            previous_treatment = self._queryset[i + 1]

            return (instance.date - previous_treatment.date).days

    def get_treatment_no(self, instance):
        for i, treatment in enumerate(reversed(self._queryset)):
            if treatment.id != instance.id:
                continue

            return i + 1

    def get_mg_per_kg(self, instance):
        if "weight_logs" not in self.context:
            return None

        for date, kilograms in self.context["weight_logs"].items():
            # ignore weight log if it was after treatment date
            if date > instance.date:
                continue

            return instance.dose_mg / kilograms

        return None

    def create(self, validated_data):
        validated_data["patient"] = Patient.objects.get(
            id=self.context["view"].kwargs["patient_pk"]
        )

        return super(TreatmentSerializer, self).create(validated_data)

    class Meta:
        model = Treatment
        fields = (
            "id",
            "days_since",
            "treatment_no",
            "stage",
            "date",
            "notes",
            "dose_mg",
            "mg_per_kg",
            "infusion_period_minutes",
            "drug_name",
            "last_updated"
        )
