from unittest.mock import patch

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_400_BAD_REQUEST,
)
from model_mommy import mommy
import pytest

from django_cryptolock.models import Address, Challenge
from .helpers import (
    VALID_BITCOIN_ADDRESS,
    VALID_MONERO_ADDRESS,
    gen_challenge,
    set_bitcoin_settings,
    set_monero_settings,
)

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.parametrize("method", ["put", "patch", "delete", "head", "options"])
def test_methods_not_allowed_for_token_login(api_client, method):
    func = getattr(api_client, method)
    response = func(reverse_lazy("api_token_login"))
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_generate_new_token_login_challenge(api_client):
    response = api_client.get(reverse_lazy("api_token_login"))
    assert response.status_code == HTTP_200_OK
    assert "challenge" in response.json().keys()
    assert "expires" in response.json().keys()


@pytest.mark.parametrize(
    "addr,set_backend,network",
    [
        (VALID_MONERO_ADDRESS, set_monero_settings, "monero"),
        (VALID_BITCOIN_ADDRESS, set_bitcoin_settings, "bitcoin"),
    ],
)
def test_token_login_fails_invalid_data(
    api_client, settings, addr, set_backend, network
):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    set_backend(settings)

    net = Address.NETWORK_BITCOIN if network == "bitcoin" else Address.NETWORK_MONERO
    user = mommy.make(User)
    mommy.make(Address, user=user, address=addr, network=net)
    challenge = gen_challenge()

    with patch(f"django_cryptolock.backends.verify_{network}_signature") as sig_mock:
        sig_mock.return_value = False
        response = api_client.post(
            reverse_lazy("api_token_login"),
            {"challenge": challenge, "address": addr, "signature": "something"},
        )

    assert response.status_code == HTTP_400_BAD_REQUEST
    errors = response.json()
    assert "Please enter a correct address or signature." in errors["__all__"]


@pytest.mark.parametrize(
    "addr,set_backend,network",
    [
        (VALID_MONERO_ADDRESS, set_monero_settings, "monero"),
        (VALID_BITCOIN_ADDRESS, set_bitcoin_settings, "bitcoin"),
    ],
)
def test_token_login_succeeds(api_client, settings, addr, set_backend, network):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    set_backend(settings)

    net = Address.NETWORK_BITCOIN if network == "bitcoin" else Address.NETWORK_MONERO
    user = mommy.make(User)
    mommy.make(Address, user=user, address=addr, network=net)
    challenge = gen_challenge()

    with patch(f"django_cryptolock.backends.verify_{network}_signature") as sig_mock:
        sig_mock.return_value = True
        response = api_client.post(
            reverse_lazy("api_token_login"),
            {"challenge": challenge, "address": addr, "signature": "something"},
        )

    assert response.status_code == HTTP_200_OK
    assert "token" in response.json().keys()


@pytest.mark.parametrize("method", ["put", "patch", "delete", "head", "options"])
def test_methods_not_allowed_for_sign_up(api_client, method):
    func = getattr(api_client, method)
    response = func(reverse_lazy("api_signup"))
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_generate_new_sign_up_challenge(api_client):
    response = api_client.get(reverse_lazy("api_signup"))
    assert response.status_code == HTTP_200_OK
    assert "challenge" in response.json().keys()
    assert "expires" in response.json().keys()


def test_sign_up_fails_no_input(api_client):
    response = api_client.post(reverse_lazy("api_signup"))
    errors = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "This field is required." in errors["challenge"]
    assert "This field is required." in errors["address"]
    assert "This field is required." in errors["signature"]
    assert "This field is required." in errors["username"]


@pytest.mark.parametrize(
    "addr,set_backend",
    [
        (VALID_MONERO_ADDRESS, set_monero_settings),
        (VALID_BITCOIN_ADDRESS, set_bitcoin_settings),
    ],
)
def test_sign_up_fails_duplicate_address(api_client, settings, addr, set_backend):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    set_backend(settings)
    challenge = gen_challenge()
    mommy.make(Address, address=addr)
    response = api_client.post(
        reverse_lazy("api_signup"),
        {
            "challenge": challenge,
            "address": addr,
            "signature": "something",
            "username": "user",
        },
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    errors = response.json()
    assert "This address already exists" in errors["address"]


@pytest.mark.parametrize(
    "addr,set_backend",
    [
        (VALID_MONERO_ADDRESS, set_monero_settings),
        (VALID_BITCOIN_ADDRESS, set_bitcoin_settings),
    ],
)
def test_sign_up_fails_invalid_signature(api_client, settings, addr, set_backend):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    set_backend(settings)
    challenge = gen_challenge()

    with patch("django_cryptolock.api_views.verify_signature") as sig_mock:
        sig_mock.return_value = False
        response = api_client.post(
            reverse_lazy("api_signup"),
            {
                "challenge": challenge,
                "address": addr,
                "signature": "something",
                "username": "user",
            },
        )

    assert response.status_code == HTTP_400_BAD_REQUEST
    errors = response.json()
    assert "Invalid signature" in errors["signature"]


@pytest.mark.parametrize(
    "addr,set_backend",
    [
        (VALID_MONERO_ADDRESS, set_monero_settings),
        (VALID_BITCOIN_ADDRESS, set_bitcoin_settings),
    ],
)
def test_sign_up_succeeds(api_client, settings, addr, set_backend):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    set_backend(settings)
    challenge = gen_challenge()

    with patch("django_cryptolock.api_views.verify_signature") as sig_mock:
        sig_mock.return_value = True
        response = api_client.post(
            reverse_lazy("api_signup"),
            {
                "challenge": challenge,
                "address": addr,
                "signature": "something",
                "username": "user",
            },
        )

    assert response.status_code == HTTP_201_CREATED
