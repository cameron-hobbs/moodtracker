import pytest
from rest_framework.test import APIClient

from patient.tests.factories import *
from treatment.tests.factories import *
from tracker.tests.factories import *


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, custom_user_factory):
    user = custom_user_factory(username="cameron", password="testing", patient=None)
    api_client.force_authenticate(user)
    return user


@pytest.fixture
def another_user(custom_user_factory):
    return custom_user_factory(
        username="matt", password="testing", patient=None
    )
