from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from tracker.models import MoodTracker
from tracker.serializers import MoodTrackerSerializer


class MoodTrackerView(ReadOnlyModelViewSet):
    serializer_class = MoodTrackerSerializer
    queryset = MoodTracker.objects.none()

    def get_queryset(self):
        patient_id = self.kwargs["patient_pk"]
        queryset = self.request.user.get_patients()

        client = queryset.filter(patient_id=patient_id).first()

        if client is None:
            return self.queryset

        return client.patient.mood_tracker_scores.order_by("-date")

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)
