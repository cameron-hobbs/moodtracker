import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from treatment.models import Treatment
from datetime import date


@register
class TreatmentFactory(DjangoModelFactory):
    dose_mg = factory.Faker("pyfloat", min_value=0, max_value=250)
    date = date.today()

    class Meta:
        model = Treatment
