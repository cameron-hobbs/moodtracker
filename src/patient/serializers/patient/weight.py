from rest_framework.serializers import ModelSerializer

from patient.models import WeightLog


class WeightLogSerializer(ModelSerializer):
    class Meta:
        model = WeightLog
        fields = ["kilograms", "date"]
