from datetime import timedelta, date

import pytest
from rest_framework import status


@pytest.mark.django_db
def test_treatment_list_idor(
    authenticated_user,
    another_user,
    patient_factory,
    custom_user_factory,
    treatment_factory,
    api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    another_user.clients.add(target)

    for day in range(1, 5):
        treatment_date = date.today() + timedelta(days=day)
        treatment = treatment_factory(patient=target.patient)
        treatment.date = treatment_date
        treatment.save()

    url = f"/api/mood_tracker/patient/{target.patient_id}/treatment/"

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

    assert len(res.json()) == 0


@pytest.mark.django_db
def test_treatment_create_idor(
    authenticated_user,
    another_user,
    patient_factory,
    custom_user_factory,
    api_client
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

    api_client.force_authenticate(another_user)

    assert len(api_client.get(url).json()) == 0


@pytest.mark.django_db
def test_treatment_update_notes(
    authenticated_user,
    another_user,
    patient_factory,
    custom_user_factory,
    treatment_factory,
    api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    another_user.clients.add(target)

    treatment = treatment_factory(patient=target.patient)

    url = f"/api/mood_tracker/patient/{target.patient_id}/treatment/{treatment.id}/"

    data = {
        "notes": "Hello world"
    }

    res = api_client.patch(url, data=data, format="json")

    assert res.status_code == status.HTTP_404_NOT_FOUND
