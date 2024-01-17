import pytest
from django.contrib.auth.hashers import make_password
from rest_framework import status


@pytest.mark.django_db
def test_access_token(api_client, custom_user_factory):
    custom_user_factory(
        username="cameron", password=make_password("testing"), patient=None
    )

    url = "/api/auth/token/"

    res = api_client.post(url, data={
        "username": "cameron",
        "password": "testing"
    }, format="json")

    assert res.status_code == status.HTTP_200_OK
    result = res.json()

    assert result["access"]
    assert result["refresh"]


@pytest.mark.django_db
def test_refresh_token(api_client, custom_user_factory):
    custom_user_factory(
        username="cameron", password=make_password("testing"), patient=None
    )

    url = "/api/auth/token/"

    refresh_token = api_client.post(url, data={
        "username": "cameron",
        "password": "testing"
    }, format="json").json()["refresh"]

    refresh_url = "/api/auth/token/refresh/"

    res = api_client.post(refresh_url, data={"refresh": refresh_token}, format="json")

    assert res.status_code == status.HTTP_200_OK

    assert res.json()["access"]
