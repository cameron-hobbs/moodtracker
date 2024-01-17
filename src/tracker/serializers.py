from rest_framework.serializers import ModelSerializer

from tracker.models import MoodTracker


class MoodTrackerSerializer(ModelSerializer):
    class Meta:
        model = MoodTracker
        fields = ["date", "mood_score"]
