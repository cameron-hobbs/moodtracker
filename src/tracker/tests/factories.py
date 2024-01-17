import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from tracker.models import MoodTracker


@register
class MoodTrackerFactory(DjangoModelFactory):
    mood_score = factory.Faker("pyint", min_value=1, max_value=10)

    class Meta:
        model = MoodTracker
