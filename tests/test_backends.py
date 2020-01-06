from unittest.mock import MagicMock, patch

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

import pytest
from model_mommy import mommy

from django_cryptolock.models import Address

VALID_ADDRESS = "46fYuhPAdsxMbEeMg97LhSbFPamdiCw7C6b19VEcZSmV6xboWFZuZQ9MTbj1wLszhUExHi63CMtsWjDTrRDqegZiPVebgYq"
User = get_user_model()

pytestmark = pytest.mark.django_db

DUMMY_CREDS = {"username": "test", "password": "insecure"}


@pytest.fixture
def existing_user():
    return User.objects.create_user(**DUMMY_CREDS)


def test_monero_backend_receives_insuficient_data(existing_user):
    user = authenticate(MagicMock(), username="test")
    assert user is None


def test_monero_backend_lets_the_next_backend_to_be_used(existing_user):
    user = authenticate(MagicMock(), **DUMMY_CREDS)
    assert user is not None


def test_monero_backend_does_not_find_address(existing_user):
    user = authenticate(
        MagicMock(), address=VALID_ADDRESS, challeng="1", signature="somesig"
    )
    assert user is None


def test_monero_backend_cannot_connect_to_RPC(existing_user):
    mommy.make(Address, address=VALID_ADDRESS, user=existing_user)

    user = authenticate(
        MagicMock(),
        address=VALID_ADDRESS,
        challenge="1",
        signature="invalid sig",
        **DUMMY_CREDS
    )

    assert user is None


def test_monero_backend_invalid_signature(existing_user):
    mommy.make(Address, address=VALID_ADDRESS, user=existing_user)

    with patch("django_cryptolock.backends.verify_signature") as verify_mock:
        verify_mock.return_value = False
        user = authenticate(
            MagicMock(), address=VALID_ADDRESS, challenge="1", signature="invalid sig"
        )

    assert user is None


def test_monero_backed_valid_signature(existing_user):
    mommy.make(Address, address=VALID_ADDRESS, user=existing_user)

    with patch("django_cryptolock.backends.verify_signature") as verify_mock:
        verify_mock.return_value = True
        user = authenticate(
            MagicMock(), address=VALID_ADDRESS, challenge="1", signature="valid sig"
        )

    assert user == existing_user
