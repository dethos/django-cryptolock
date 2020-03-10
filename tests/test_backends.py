from unittest.mock import MagicMock, patch

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

import pytest
from model_mommy import mommy

from django_cryptolock.models import Address

User = get_user_model()
pytestmark = pytest.mark.django_db

DUMMY_CREDS = {"username": "test", "password": "insecure"}
VALID_MONERO_ADDRESS = "46fYuhPAdsxMbEeMg97LhSbFPamdiCw7C6b19VEcZSmV6xboWFZuZQ9MTbj1wLszhUExHi63CMtsWjDTrRDqegZiPVebgYq"
VALID_BITCOIN_ADDRESS = "1N5attoW1FviYGnLmRu9xjaPMKTkWxtUCW"
VALID_BITCOIN_SIG = "H5wI5uqhRCxBpyre2mYkjLxNKPi/TCj9IaHhmfnF8Wn1Pac6gsuYsd2GqTNpy/JFDv3HBSOD75pk2OsGDxE7U4o="
VALID_BITID_URI = "bitid://www.django-cryptolock.test/?x=44d91949c7b2eb20"
EXAMPLE_LOGIN_URL = "https://www.django-cryptolock.test/"


def set_monero_settings(settings):
    settings.AUTHENTICATION_BACKENDS = [
        "django_cryptolock.backends.MoneroAddressBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]


def set_bitcoin_settings(settings):
    settings.AUTHENTICATION_BACKENDS = [
        "django_cryptolock.backends.BitcoinAddressBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]


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
