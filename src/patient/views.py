from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from patient.models import CustomUser
from patient.serializers import PatientFullSerializer, PatientOverviewSerializer


class PatientView(ModelViewSet):
    serializer_class = PatientFullSerializer
    queryset = CustomUser.objects.none()
    ordering_fields = ["pk"]
    ordering = ["-pk"]

    def get_queryset(self):
        queryset = self.request.user.get_patients()

        if self.action == "retrieve" or self.action == "update":
            return queryset.preload_patient()

        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, patient_id=self.kwargs["pk"])

    def get_serializer_class(self):
        if self.action == "list":
            return PatientOverviewSerializer

        return self.serializer_class

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)
