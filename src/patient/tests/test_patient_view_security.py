from datetime import date

import pytest
from faker import Faker
from rest_framework import status


@pytest.mark.django_db
def test_patient_list_idor(
    api_client, authenticated_user, another_user, custom_user_factory
):
    patients = custom_user_factory.create_batch(10)

    another_user.clients.set(patients)

    res = api_client.get("/api/mood_tracker/patient/")

    assert res.status_code == status.HTTP_200_OK

    assert len(res.json()) == 0


@pytest.mark.django_db
def test_patient_edit_idor(
    api_client, authenticated_user, another_user, custom_user_factory
):
    target = custom_user_factory()

    another_user.clients.add(target)

    update_data = {
        "first_name": "Gary",
        "last_name": "Hoffman",
        "email": "martinkaren@example.org",
        "patient": {
            "date_of_birth": "2022-11-23",
            "sex": "male",
            "primary_contact_no": "+447775230895",
            "primary_diagnosis": "Anxiety",
            "secondary_contact_no": None,
            "address": "USNV Martinez\nFPO AP 60468",
            "occupation": "Conservator, furniture",
            "gp": {
                "name": "Megan Miller",
                "primary_contact_no": "+447775230895",
                "secondary_contact_no": None,
                "email": "juliebryant@example.com",
                "address": "297 Russell Falls Apt. 627\nWest Taylorview, GA 08703"
            },
            "next_of_kin": {
                "name": "Christopher Webb",
                "primary_contact_no": "+447775230895",
                "secondary_contact_no": None,
                "email": "castroadam@example.org",
                "address": "25615 Copeland Mount Suite 526\nWest Janeshire, WI 71289"
            },
            "physciatrist": {
                "name": "Carrie Bennett",
                "primary_contact_no": "+447775230895",
                "secondary_contact_no": None,
                "email": "andreacollins@example.org",
                "address": "6392 Jason Coves Suite 607\nGlasshaven, IN 33370"
            },
            "allergies": None,
            "current_medication": None,
            "other_notes": None,
            "weight_log": [{
                "date": "2022-11-23",
                "kilograms": 67
            }]
        }
    }

    res = api_client.put(f"/api/mood_tracker/patient/{target.pk}/", data=update_data, format="json")

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_patient_create_idor(api_client, another_user, authenticated_user):
    def _generate_support_data():
        fake = Faker()
        yield {
            "name": fake.name(),
            "primary_contact_no": "+447775230895",
            "secondary_contact_no": None,
            "address": fake.address(),
            "email": fake.email()
        }

    data = {
        "first_name": "Cameron",
        "last_name": "Hobbs",
        "patient": {
            "date_of_birth": date(year=1998, month=8, day=25).isoformat(),
            "sex": "male",
            "primary_contact_no": "+447775230895",
            "primary_diagnosis": "anxiety",
            "address": "14 Downing street",
            "occupation": "Software developer",
            "gp": next(_generate_support_data()),
            "next_of_kin": next(_generate_support_data()),
            "physciatrist": next(_generate_support_data()),
            "weight_log": [
                {
                    "kilograms": 71,
                    "date": date.today().isoformat()
                }
            ]
        }
    }

    res = api_client.post("/api/mood_tracker/patient/", data=data, format="json")

    assert res.status_code == status.HTTP_201_CREATED

    api_client.force_authenticate(another_user)

    assert len(api_client.get("/api/mood_tracker/patient/").json()) == 0
