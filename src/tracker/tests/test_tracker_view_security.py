import pytest
from rest_framework import status


@pytest.mark.django_db
def test_tracker_list_idor(
    authenticated_user,
    another_user,
    custom_user_factory,
    patient_factory,
    mood_tracker_factory,
    api_client
):
    target = custom_user_factory()
    target.patient = patient_factory()
    target.save()

    another_user.clients.add(target)

    mood_tracker_factory.create_batch(5, patient=target.patient)

    url = f"/api/mood_tracker/patient/{target.patient.id}/tracker/"

    res = api_client.get(url)

    assert res.status_code == status.HTTP_200_OK

    assert len(res.json()) == 0
