from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model

import pytest
from model_mommy import mommy

from django_cryptolock.forms import SimpleLoginForm, SimpleSignUpForm
from django_cryptolock.models import Address

from .helpers import set_monero_settings, set_bitcoin_settings

pytestmark = pytest.mark.django_db

VALID_MONERO_ADDRESS = "46fYuhPAdsxMbEeMg97LhSbFPamdiCw7C6b19VEcZSmV6xboWFZuZQ9MTbj1wLszhUExHi63CMtsWjDTrRDqegZiPVebgYq"
VALID_BITCOIN_ADDRESS = "1N5attoW1FviYGnLmRu9xjaPMKTkWxtUCW"
User = get_user_model()


def test_simpleloginform_generates_new_challenge():
    request = MagicMock()
    initial = {}
    request.session.__setitem__.side_effect = initial.__setitem__
    request.session.__getitem__.side_effect = initial.__getitem__
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleLoginForm(request=request)
    assert form.initial.get("challenge")
    assert initial["current_challenge"] == form.initial.get("challenge")
    assert form.initial.get("challenge").startswith("bitid://something")


def test_simpleloginform_generates_no_new_challenge():
    request = MagicMock()
    initial = {}
    request.session.__setitem__.side_effect = initial.__setitem__
    request.session.__getitem__.side_effect = initial.__getitem__
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleLoginForm(request=request, data={"address": ""})
    assert not form.initial.get("challenge")
    assert not initial.get("current_challenge")


@pytest.mark.django_db
def test_simpleloginform_valid_data(settings):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleLoginForm(
        request=request,
        data={
            "address": VALID_MONERO_ADDRESS,
            "challenge": "12345678",
            "signature": "some valid signature",
        },
    )
    with patch("django_cryptolock.forms.authenticate") as auth_mock:
        auth_mock.return_value = mommy.make(User)
        request.session.get.return_value = "12345678"
        assert form.is_valid()


def test_simplesignupform_generates_new_challenge():
    request = MagicMock()
    initial = {}
    request.session.__setitem__.side_effect = initial.__setitem__
    request.session.__getitem__.side_effect = initial.__getitem__
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleSignUpForm(request=request)
    assert form.initial.get("challenge")
    assert initial["current_challenge"] == form.initial.get("challenge")
    assert form.initial.get("challenge").startswith("bitid://something")


def test_simplesignupform_generates_no_new_challenge():
    request = MagicMock()
    initial = {}
    request.session.__setitem__.side_effect = initial.__setitem__
    request.session.__getitem__.side_effect = initial.__getitem__
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleSignUpForm(request=request, data={"address": ""})
    assert not form.initial.get("challenge")
    assert not initial.get("current_challenge")


def test_validate_address_unique(settings):
    settings.DJCL_MONERO_NETWORK = "mainnet"
    mommy.make(Address, address=VALID_MONERO_ADDRESS)
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleSignUpForm(
        request=request,
        data={
            "username": "foo",
            "address": VALID_MONERO_ADDRESS,
            "challenge": "12345678",
            "signature": "some valid signature",
        },
    )
    assert not form.is_valid()
    assert "This address already exists" in form.errors["address"]


def test_simplesignupform_validate_bitcoin_addr(settings):
    set_bitcoin_settings(settings)
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    request.session.get.return_value = "12345678"
    form = SimpleSignUpForm(
        request=request,
        data={
            "username": "foo",
            "address": VALID_BITCOIN_ADDRESS,
            "challenge": "12345678",
            "signature": "some valid signature",
        },
    )
    assert form.is_valid()


def test_simplesignupform_valid_monero_addr(settings):
    set_monero_settings(settings)
    settings.DJCL_MONERO_NETWORK = "mainnet"
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    request.session.get.return_value = "12345678"
    form = SimpleSignUpForm(
        request=request,
        data={
            "username": "foo",
            "address": VALID_MONERO_ADDRESS,
            "challenge": "12345678",
            "signature": "some valid signature",
        },
    )
    assert form.is_valid()


def test_simplesignupform_validate_invalid_addr():
    request = MagicMock()
    request.build_absolute_uri.return_value = "http://something/"
    form = SimpleSignUpForm(
        request=request,
        data={
            "username": "foo",
            "address": "bad addr",
            "challenge": "12345678",
            "signature": "some valid signature",
        },
    )
    assert not form.is_valid()
    assert "Invalid address" in form.errors["address"]
