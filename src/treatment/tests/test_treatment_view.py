from datetime import timedelta, date, datetime

import pytest
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
def test_treatment_list(
    authenticated_user,
    patient_factory,
    custom_user_factory,
    treatment_factory,
    api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    authenticated_user.clients.add(target)

    for day in range(1, 5):
        treatment_date = date.today() + timedelta(days=day)
        treatment = treatment_factory(patient=target.patient)
        treatment.date = treatment_date
        treatment.save()

    url = f"/api/mood_tracker/patient/{target.patient_id}/treatment/"

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

    i = 4

    for treatment in res.json():
        assert treatment["days_since"] == (1 if i > 1 else None)
        assert treatment["date"]
        assert treatment["dose_mg"]
        assert "infusion_period_minutes" in treatment
        assert "mg_per_kg" in treatment
        assert "notes" in treatment
        assert "stage" in treatment
        assert treatment["treatment_no"] == i
        i = i - 1


@pytest.mark.django_db
def test_treatment_create(
    authenticated_user, patient_factory, custom_user_factory, api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    data = {
        "dose_mg": 250.0,
        "date": "2022-01-06",
        "drug_name": "Setraline",
        "infusion_period_minutes": 40,
        "stage": 1
    }

    url = f"/api/mood_tracker/patient/{target.patient_id}/treatment/"

    res = api_client.post(url, data=data, format="json")

    assert res.status_code == status.HTTP_201_CREATED

    result = res.json()

    result.pop("id")
    result.pop("days_since")
    result.pop("mg_per_kg")
    result.pop("notes")
    result.pop("treatment_no")
    result.pop("last_updated")
    assert result == data


@pytest.mark.django_db
def test_treatment_update_notes(
    authenticated_user,
    patient_factory,
    custom_user_factory,
    treatment_factory,
    api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    authenticated_user.clients.add(target)

    treatment = treatment_factory(patient=target.patient)

    url = f"/api/mood_tracker/patient/{target.patient_id}/treatment/{treatment.id}/"

    data = {
        "notes": "Hello world"
    }

    res = api_client.patch(url, data=data, format="json")

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["notes"] == data["notes"]


@pytest.mark.django_db
def test_treatment_update_infusion_period(
    authenticated_user,
    patient_factory,
    custom_user_factory,
    treatment_factory,
    api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    authenticated_user.clients.add(target)

    treatment = treatment_factory(patient=target.patient)

    url = f"/api/mood_tracker/patient/{target.patient_id}/treatment/{treatment.id}/"

    data = {
        "infusion_period_minutes": 60
    }

    res = api_client.patch(url, data=data, format="json")

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["infusion_period_minutes"] == data["infusion_period_minutes"]


@pytest.mark.django_db
def test_treatment_update_dose_mg(
    authenticated_user,
    patient_factory,
    custom_user_factory,
    treatment_factory,
    api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    authenticated_user.clients.add(target)

    treatment = treatment_factory(patient=target.patient)

    url = f"/api/mood_tracker/patient/{target.patient_id}/treatment/{treatment.id}/"

    data = {
        "dose_mg": 50
    }

    res = api_client.patch(url, data=data, format="json")

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["dose_mg"] == data["dose_mg"]


@pytest.mark.django_db
def test_treatment_update_date(
    authenticated_user,
    patient_factory,
    custom_user_factory,
    treatment_factory,
    api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    authenticated_user.clients.add(target)

    treatment = treatment_factory(patient=target.patient)

    url = f"/api/mood_tracker/patient/{target.patient_id}/treatment/{treatment.id}/"

    data = {
        "date": str(date.today())
    }

    res = api_client.patch(url, data=data, format="json")

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["date"].replace("T", " ").replace("Z", "") == data["date"]
