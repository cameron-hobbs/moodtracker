from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from patient.models import WeightLog
from treatment.models import Treatment
from treatment.serializers import TreatmentSerializer, TreatmentPartialUpdateSerializer


class TreatmentView(ModelViewSet):
    queryset = Treatment.objects.none()
    serializer_class = TreatmentSerializer

    def get_queryset(self):
        patient_id = self.kwargs["patient_pk"]
        queryset = self.request.user.get_patients()

        client = queryset.filter(patient_id=patient_id).first()

        if client is None:
            return self.queryset

        return client.patient.treatments.order_by("-date")

    def get_serializer_context(self):
        context = super(TreatmentView, self).get_serializer_context()

        patient_id = self.kwargs["patient_pk"]
        queryset = self.request.user.get_patients()

        client = queryset.filter(patient_id=patient_id).first()

        if client is None:
            return context

        context["weight_logs"] = {
            log.date: log.kilograms
            for log in WeightLog.objects.filter(patient=client.patient).order_by("-date")
        }

        return context

    def get_serializer_class(self):
        if self.action == "partial_update":
            return TreatmentPartialUpdateSerializer

        return self.serializer_class

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        if kwargs.get("partial"):
            return super(TreatmentView, self).update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)
