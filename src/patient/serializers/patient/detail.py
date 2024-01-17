from datetime import date
from uuid import uuid4

from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from patient.models import CustomUser, Patient, PatientSupport, WeightLog
from patient.serializers.patient.weight import WeightLogSerializer


class _PatientSupportSerializer(ModelSerializer):
    class Meta:
        model = PatientSupport
        fields = ["name", "primary_contact_no", "secondary_contact_no", "email", "address"]


class _PatientDetailSerializer(ModelSerializer):
    gp = _PatientSupportSerializer(required=False)
    next_of_kin = _PatientSupportSerializer(required=False)
    physciatrist = _PatientSupportSerializer(required=False)

    primary_contact_no = CharField(required=True)
    primary_diagnosis = CharField(required=True)
    weight_log = WeightLogSerializer(required=True, many=True)

    def validate(self, attrs):
        if not len(attrs.get("weight_log", [])):
            raise ValidationError("Weight log cannot be empty")

        return super(_PatientDetailSerializer, self).validate(attrs)

    class Meta:
        model = Patient
        fields = [
            "id",
            "date_of_birth",
            "sex",
            "primary_contact_no",
            "primary_diagnosis",
            "secondary_contact_no",
            "address",
            "occupation",
            "gp",
            "next_of_kin",
            "physciatrist",
            "allergies",
            "current_medication",
            "other_notes",
            "weight_log"
        ]


class PatientFullSerializer(ModelSerializer):
    patient = _PatientDetailSerializer(required=True)

    first_name = CharField(required=True)
    last_name = CharField(required=True)

    @classmethod
    def _create_or_update_patient_support(cls, patient, key, support_data):
        if support_data is None:
            return None

        support_member = getattr(patient, key)

        if support_member is None:
            support_member = PatientSupport()

        support_member.address = support_data.get("address")
        support_member.name = support_data.get("name")
        support_member.email = support_data.get("email")
        support_member.primary_contact_no = support_data.get("primary_contact_no")
        support_member.secondary_contact_no = support_data.get("secondary_contact_no")
        support_member.save()

        return support_member

    def update(self, instance, validated_data):
        patient_data = validated_data.pop("patient")
        nok = patient_data.pop("next_of_kin", None)
        gp = patient_data.pop("gp", None)
        physc = patient_data.pop("physciatrist", None)
        weight_log = patient_data.pop("weight_log", [])

        with transaction.atomic():
            instance.patient.next_of_kin = self._create_or_update_patient_support(
                instance.patient, "next_of_kin", nok
            )
            instance.patient.gp = self._create_or_update_patient_support(
                instance.patient, "gp", gp
            )
            instance.patient.physciatrist = self._create_or_update_patient_support(
                instance.patient, "physciatrist", physc
            )

            for log in weight_log:
                weight, _ = WeightLog.objects.get_or_create(
                    patient=instance.patient, date=date.today(), defaults=dict(
                        kilograms=log["kilograms"]
                    )
                )

            for key, val in patient_data.items():
                setattr(instance.patient, key, val)

            for key, val in validated_data.items():
                setattr(instance, key, val)

            instance.save()

        return instance

    def create(self, validated_data):
        patient_data = validated_data.pop("patient")

        weight_log = patient_data.pop("weight_log")

        nok = patient_data.pop("next_of_kin", None)
        gp = patient_data.pop("gp", None)
        physc = patient_data.pop("physciatrist", None)

        with transaction.atomic():
            patient = Patient(**patient_data)

            patient.next_of_kin = self._create_or_update_patient_support(
                patient, "next_of_kin", nok
            )
            patient.gp = self._create_or_update_patient_support(
                patient, "gp", gp
            )
            patient.physciatrist = self._create_or_update_patient_support(
                patient, "physciatrist", physc
            )
            patient.save()

            WeightLog.objects.bulk_create([
                WeightLog(patient=patient, date=date.today(), kilograms=log["kilograms"])
                for log in weight_log
            ], ignore_conflicts=True)

            custom_user, _ = CustomUser.objects.get_or_create(
                patient=patient,
                clinician=self.context["request"].user,
                defaults={
                    "username": uuid4().hex,
                    **validated_data
                }
            )

        return custom_user

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "patient"]
