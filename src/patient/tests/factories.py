from datetime import date

import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from patient.models import CustomUser, Patient, PatientSupport


@register
class PatientSupportFactory(DjangoModelFactory):
    name = factory.Faker("name")
    primary_contact_no = factory.Faker("phone_number")
    secondary_contact_no = factory.Faker("phone_number")
    email = factory.Faker("email")
    address = factory.Faker("address")

    class Meta:
        model = PatientSupport


@register
class PatientFactory(DjangoModelFactory):
    date_of_birth = date.today()
    sex = "male"
    primary_contact_no = factory.Faker("phone_number")
    address = factory.Faker("address")
    occupation = factory.Faker("job")

    allergies = None
    current_medication = None
    other_notes = None

    next_of_kin = factory.SubFactory(PatientSupportFactory)
    gp = factory.SubFactory(PatientSupportFactory)
    physciatrist = factory.SubFactory(PatientSupportFactory)

    class Meta:
        model = Patient


@register
class CustomUserFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    username = factory.Faker("name")
    patient = factory.SubFactory(PatientFactory)

    class Meta:
        model = CustomUser

