from unittest.mock import MagicMock, patch

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

import pytest
from model_mommy import mommy

from django_cryptolock.models import Address

from .helpers import (
    set_monero_settings,
    set_bitcoin_settings,
    DUMMY_CREDS,
    VALID_BITCOIN_ADDRESS,
    VALID_BITCOIN_SIG,
    VALID_BITID_URI,
    VALID_MONERO_ADDRESS,
    EXAMPLE_LOGIN_URL,
)

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def existing_user():
    return User.objects.create_user(**DUMMY_CREDS)


def test_monero_backend_receives_insuficient_data(settings, existing_user):
    set_monero_settings(settings)
    user = authenticate(MagicMock(), username="test")
    assert user is None


def test_monero_backend_lets_the_next_backend_to_be_used(settings, existing_user):
    set_monero_settings(settings)
    user = authenticate(MagicMock(), **DUMMY_CREDS)
    assert user is not None


def test_monero_backend_does_not_find_address(settings, existing_user):
    set_monero_settings(settings)
    user = authenticate(
        MagicMock(), address=VALID_MONERO_ADDRESS, challeng="1", signature="somesig"
    )
    assert user is None


def test_monero_backend_cannot_connect_to_RPC(settings, existing_user):
    set_monero_settings(settings)
    mommy.make(Address, address=VALID_MONERO_ADDRESS, user=existing_user)

    user = authenticate(
        MagicMock(),
        address=VALID_MONERO_ADDRESS,
        challenge="1",
        signature="invalid sig",
        **DUMMY_CREDS
    )

    assert user is None


def test_monero_backend_invalid_signature(settings, existing_user):
    set_monero_settings(settings)
    mommy.make(Address, address=VALID_MONERO_ADDRESS, user=existing_user)

    with patch("django_cryptolock.backends.verify_monero_signature") as verify_mock:
        verify_mock.return_value = False
        user = authenticate(
            MagicMock(),
            address=VALID_MONERO_ADDRESS,
            challenge="1",
            signature="invalid sig",
        )

    assert user is None


def test_monero_backend_valid_signature(settings, existing_user):
    set_monero_settings(settings)
    mommy.make(Address, address=VALID_MONERO_ADDRESS, user=existing_user)

    with patch("django_cryptolock.backends.verify_monero_signature") as verify_mock:
        verify_mock.return_value = True
        user = authenticate(
            MagicMock(),
            address=VALID_MONERO_ADDRESS,
            challenge="1",
            signature="valid sig",
        )

    assert user == existing_user


def test_bitcoin_backend_receives_insuficient_data(settings, existing_user):
    set_bitcoin_settings(settings)
    user = authenticate(MagicMock(), username="test")
    assert user is None


def test_bitcoin_backend_lets_the_next_backend_to_be_used(settings, existing_user):
    set_bitcoin_settings(settings)
    user = authenticate(MagicMock(), **DUMMY_CREDS)
    assert user is not None


def test_bitcoin_backend_does_not_find_address(settings, existing_user):
    set_bitcoin_settings(settings)
    user = authenticate(
        MagicMock(),
        address=VALID_BITCOIN_ADDRESS,
        bitid_uri="bitid://something",
        signature="somesig",
    )
    assert user is None


def test_bitcoin_backend_invalid_signature(settings, existing_user):
    set_bitcoin_settings(settings)
    mommy.make(
        Address,
        address=VALID_BITCOIN_ADDRESS,
        network=Address.NETWORK_BITCOIN,
        user=existing_user,
    )

    mock = MagicMock()
    mock.build_absolute_uri.return_value = EXAMPLE_LOGIN_URL

    user = authenticate(
        mock,
        address=VALID_BITCOIN_ADDRESS,
        bitid_uri=VALID_BITID_URI,
        signature="invalid sig",
    )

    assert user is None


def test_bitcoin_backend_valid_signature(settings, existing_user):
    set_bitcoin_settings(settings)
    set_bitcoin_settings(settings)
    mommy.make(
        Address,
        address=VALID_BITCOIN_ADDRESS,
        network=Address.NETWORK_BITCOIN,
        user=existing_user,
    )

    mock = MagicMock()
    mock.build_absolute_uri.return_value = EXAMPLE_LOGIN_URL

    user = authenticate(
        mock,
        address=VALID_BITCOIN_ADDRESS,
        challenge=VALID_BITID_URI,
        signature=VALID_BITCOIN_SIG,
    )

    assert user == existing_user
