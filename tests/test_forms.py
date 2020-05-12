from unittest.mock import MagicMock, patch
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

import pytest
from model_mommy import mommy
from pybitid import bitid

from django_cryptolock.forms import SimpleLoginForm, SimpleSignUpForm
from django_cryptolock.models import Address, Challenge

from .helpers import set_monero_settings, set_bitcoin_settings

pytestmark = pytest.mark.django_db

VALID_MONERO_ADDRESS = "46fYuhPAdsxMbEeMg97LhSbFPamdiCw7C6b19VEcZSmV6xboWFZuZQ9MTbj1wLszhUExHi63CMtsWjDTrRDqegZiPVebgYq"
VALID_BITCOIN_ADDRESS = "1N5attoW1FviYGnLmRu9xjaPMKTkWxtUCW"
FUTURE_TIME = timezone.now() + timedelta(minutes=15)
User = get_user_model()


def gen_challenge(request, challenge):
    return bitid.build_uri(request.build_absolute_uri(), challenge)


def test_simpleloginform_generates_new_challenge():
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    assert not Challenge.objects.all().exists()

    form = SimpleLoginForm(request=request)
    challenge = Challenge.objects.first()
    assert form.initial.get("challenge")
    assert form.initial.get("challenge") == gen_challenge(request, challenge.challenge)
    assert form.initial.get("challenge").startswith("bitid://something")


def test_simpleloginform_generates_no_new_challenge():
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    assert not Challenge.objects.all().exists()

    form = SimpleLoginForm(request=request, data={"address": ""})
    assert not Challenge.objects.all().exists()
    assert not form.initial.get("challenge")


@pytest.mark.django_db
def test_simpleloginform_valid_data(settings):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    mommy.make(Challenge, challenge="12345678", expires=FUTURE_TIME)
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"

    form = SimpleLoginForm(
        request=request,
        data={
            "address": VALID_MONERO_ADDRESS,
            "challenge": gen_challenge(request, "12345678"),
            "signature": "some valid signature",
        },
    )
    with patch("django_cryptolock.forms.authenticate") as auth_mock:
        auth_mock.return_value = mommy.make(User)
        assert form.is_valid()


@pytest.mark.django_db
def test_simpleloginform_invalid_challenge(settings):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    mommy.make(Challenge, challenge="12345678", expires=FUTURE_TIME)
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleLoginForm(
        request=request,
        data={
            "address": VALID_MONERO_ADDRESS,
            "challenge": gen_challenge(request, "1234567"),
            "signature": "some valid signature",
        },
    )
    with patch("django_cryptolock.forms.authenticate") as auth_mock:
        auth_mock.return_value = mommy.make(User)
        assert not form.is_valid()


@pytest.mark.django_db
def test_simpleloginform_expired_challenge(settings):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    mommy.make(Challenge, challenge="12345678", expires=timezone.now())
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleLoginForm(
        request=request,
        data={
            "address": VALID_MONERO_ADDRESS,
            "challenge": gen_challenge(request, "12345678"),
            "signature": "some valid signature",
        },
    )
    with patch("django_cryptolock.forms.authenticate") as auth_mock:
        auth_mock.return_value = mommy.make(User)
        assert not form.is_valid()


def test_simplesignupform_generates_new_challenge():
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    assert not Challenge.objects.all().exists()

    form = SimpleSignUpForm(request=request)
    challenge = Challenge.objects.first()
    assert form.initial.get("challenge")
    assert form.initial.get("challenge") == gen_challenge(request, challenge.challenge)
    assert form.initial.get("challenge").startswith("bitid://something")


def test_simplesignupform_generates_no_new_challenge():
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    assert not Challenge.objects.all().exists()

    form = SimpleSignUpForm(request=request, data={"address": ""})
    assert not Challenge.objects.all().exists()
    assert not form.initial.get("challenge")


def test_validate_address_unique(settings):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    mommy.make(Address, address=VALID_MONERO_ADDRESS)
    mommy.make(Challenge, challenge="12345678", expires=FUTURE_TIME)
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleSignUpForm(
        request=request,
        data={
            "username": "foo",
            "address": VALID_MONERO_ADDRESS,
            "challenge": gen_challenge(request, "12345678"),
            "signature": "some valid signature",
        },
    )
    assert not form.is_valid()
    assert "This address already exists" in form.errors["address"]


def test_simplesignupform_valid_bitcoin_addr(settings):
    set_bitcoin_settings(settings)
    mommy.make(Challenge, challenge="12345678", expires=FUTURE_TIME)

    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleSignUpForm(
        request=request,
        data={
            "username": "foo",
            "address": VALID_BITCOIN_ADDRESS,
            "challenge": gen_challenge(request, "12345678"),
            "signature": "some valid signature",
        },
    )
    assert form.is_valid()


def test_simplesignupform_valid_monero_addr(settings):
    set_monero_settings(settings)
    mommy.make(Challenge, challenge="12345678", expires=FUTURE_TIME)

    settings.DJCL_MONERO_NETWORK = "mainnet"
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleSignUpForm(
        request=request,
        data={
            "username": "foo",
            "address": VALID_MONERO_ADDRESS,
            "challenge": gen_challenge(request, "12345678"),
            "signature": "some valid signature",
        },
    )
    assert form.is_valid()


def test_simplesignupform_invalid_addr():
    mommy.make(Challenge, challenge="12345678", expires=FUTURE_TIME)
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleSignUpForm(
        request=request,
        data={
            "username": "foo",
            "address": "bad addr",
            "challenge": gen_challenge(request, "12345678"),
            "signature": "some valid signature",
        },
    )
    assert not form.is_valid()
    assert "Invalid address" in form.errors["address"]


# def test_simplesignupform_invalid_challenge():
#     pass


# def test_simple_signupform_expired_challenge():
#     pass
