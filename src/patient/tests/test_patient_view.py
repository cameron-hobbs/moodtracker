from datetime import date

import pytest
from rest_framework import status
from faker import Faker


@pytest.mark.django_db
def test_patient_list(api_client, authenticated_user, custom_user_factory):
    patients = custom_user_factory.create_batch(10)

    authenticated_user.clients.set(patients)

    res = api_client.get("/api/mood_tracker/patient/")

    assert res.status_code == status.HTTP_200_OK

    for patient_data, patient in zip(res.json(), patients):
        assert patient_data["first_name"]
        assert patient_data["last_name"]

        # assert other things


@pytest.mark.django_db
def test_patient_retrieve(api_client, authenticated_user, custom_user_factory):
    target = custom_user_factory()

    authenticated_user.clients.add(target)

    res = api_client.get(f"/api/mood_tracker/patient/{target.patient.pk}/")

    assert res.status_code == status.HTTP_200_OK

    user_data = res.json()
    assert user_data["first_name"] == target.first_name
    assert user_data["last_name"] == target.last_name
    assert user_data["email"] == target.email

    patient_data = user_data["patient"]

    assert patient_data["allergies"] == target.patient.allergies
    assert patient_data["current_medication"] == target.patient.current_medication
    assert patient_data["other_notes"] == target.patient.other_notes

    # assert other things


@pytest.mark.django_db
def test_patient_edit(api_client, authenticated_user, custom_user_factory):
    target = custom_user_factory()

    authenticated_user.clients.add(target)

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

    res = api_client.put(
        f"/api/mood_tracker/patient/{target.patient.pk}/",
        data=update_data,
        format="json"
    )

    assert res.status_code == status.HTTP_200_OK

    user_data = res.json()
    assert user_data["first_name"] == update_data["first_name"]
    assert user_data["last_name"] == update_data["last_name"]
    assert user_data["email"] == update_data["email"]

    patient_data = user_data["patient"]

    assert patient_data["allergies"] == update_data["patient"]["allergies"]
    assert patient_data["current_medication"] == update_data["patient"]["current_medication"]
    assert patient_data["other_notes"] == update_data["patient"]["other_notes"]

    # assert other things


@pytest.mark.django_db
def test_patient_create_missing_required_fields(
    api_client, authenticated_user
):
    url = "/api/mood_tracker/patient/"

    res = api_client.post(url, data={}, format="json")

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.json() == {
        "first_name": ["This field is required."],
        "last_name": ["This field is required."],
        "patient": ["This field is required."]
    }

    res2 = api_client.post(url, data={
        "first_name": "Cameron",
        "last_name": "Hobbs",
        "patient": {}
    }, format="json")

    assert res2.json() == {
        "patient": {
            "primary_contact_no": ["This field is required."],
            "primary_diagnosis": ["This field is required."],
            "weight_log": ["This field is required."]
        }
    }


@pytest.mark.django_db
def test_patient_create_only_required_fields(api_client, authenticated_user):
    url = "/api/mood_tracker/patient/"

    res = api_client.post(url, data={
        "first_name": "Cameron",
        "last_name": "Hobbs",
        "patient": {
            "gp": {},
            "next_of_kin": {},
            "physciatrist": {},
            "primary_contact_no": "+447775230895",
            "primary_diagnosis": "Anxiety",
            "weight_log": [{
                "date": date.today(),
                "kilograms": 75
            }]
        }
    }, format="json")

    assert res.status_code == status.HTTP_201_CREATED

    res.json()["patient"].pop("id")

    assert res.json() == {
        "first_name": "Cameron",
        "last_name": "Hobbs",
        "email": "",
        "patient": {
            "date_of_birth": None,
            "sex": None,
            "primary_contact_no": "+447775230895",
            "primary_diagnosis": "Anxiety",
            "secondary_contact_no": None,
            "address": None,
            "occupation": None,
            "gp": {
                "name": None,
                "primary_contact_no": None,
                "secondary_contact_no": None,
                "email": None,
                "address": None
            },
            "next_of_kin": {
                "name": None,
                "primary_contact_no": None,
                "secondary_contact_no": None,
                "email": None,
                "address": None
            },
            "physciatrist": {
                "name": None,
                "primary_contact_no": None,
                "secondary_contact_no": None,
                "email": None,
                "address": None
            },
            "allergies": None,
            "current_medication": None,
            "other_notes": None,
            "weight_log": [{
                "date": str(date.today()),
                "kilograms": 75
            }]
        }
    }


@pytest.mark.django_db
def test_patient_create(api_client, authenticated_user):
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

    # assert fields
