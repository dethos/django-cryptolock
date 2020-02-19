#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-cryptolock
------------

Tests for `django-cryptolock` models module.
"""
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import pytest
from model_mommy import mommy

from django_cryptolock.models import Address

VALID_MONERO_MAINNET_ADDR = "45D8b4XiUdz86FwztAJHVeLnQqGHQUqiHSwZe6rXFHSoXw522dPdixsdi7JAGsfJsfHRCP94UFhY5W3U8KCBhsRNUSLbYFk"
VALID_MONERO_STAGENET_ADDR = "55LTR8KniP4LQGJSPtbYDacR7dz8RBFnsfAKMaMuwUNYX6aQbBcovzDPyrQF9KXF9tVU6Xk3K8no1BywnJX6GvZX8yJsXvt"
VALID_MONERO_TESTNET_ADDR = "9vmn8Vyxh6JEVmPr4qTcj3ND3FywDpMXH2fVLLEARyKCJTc3jWjxeWcbRNcaa57Bj36cARBSfWnfS89oFVKBBvGTAegdRxG"

VALID_BITCOIN_TESTNET_ADDR = "n47QBape2PcisN2mkHR2YnhqoBr56iPhJh"
VALID_BITCOIN_MAINNET_ADDR = "1AUeWMGD9hDYtAhZGZLmDjEzKSrPow4zNt"

pytestmark = pytest.mark.django_db


def test_valid_monero_mainnet_address(settings):
    settings.DJCL_MONERO_NETWORK = "mainnet"

    addr = mommy.make(Address, address=VALID_MONERO_MAINNET_ADDR)
    addr.full_clean()


def test_valid_monero_stagenet_addr(settings):
    settings.DJCL_MONERO_NETWORK = "stagenet"

    addr = mommy.make(Address, address=VALID_MONERO_STAGENET_ADDR)
    addr.full_clean()


def test_valid_monero_testnet_addr(settings):
    settings.DJCL_MONERO_NETWORK = "testnet"

    addr = mommy.make(Address, address=VALID_MONERO_TESTNET_ADDR)
    addr.full_clean()


def test_valid_bitcoin_mainnet_address(settings):
    settings.DJCL_BITCOIN_NETWORK = "mainnet"

    addr = mommy.make(
        Address, address=VALID_BITCOIN_MAINNET_ADDR, network=Address.NETWORK_BITCOIN
    )
    addr.full_clean()


def test_valid_bitcoin_testnet_address(settings):
    settings.DJCL_BITCOIN_NETWORK = "testnet"

    addr = mommy.make(
        Address, address=VALID_BITCOIN_TESTNET_ADDR, network=Address.NETWORK_BITCOIN
    )
    addr.full_clean()


def test_invalid_address():
    bad_addr = "Verywrongaddress"
    addr = mommy.make(Address, address=bad_addr)

    with pytest.raises(ValidationError) as error:
        addr.full_clean()

    assert (
        "Invalid address for the given network" in error.value.message_dict["__all__"]
    )


def test_wrong_monero_network_address(settings):
    settings.DJCL_MONERO_NETWORK = "stagenet"
    addr = mommy.make(Address, address=VALID_MONERO_MAINNET_ADDR)

    with pytest.raises(ValidationError) as error:
        addr.full_clean()

    assert (
        "Invalid address for the given network" in error.value.message_dict["__all__"]
    )


def test_wrong_bitcoin_network_address(settings):
    settings.DJCL_BITCOIN_NETWORK = "testnet"
    addr = mommy.make(
        Address, address=VALID_BITCOIN_MAINNET_ADDR, network=Address.NETWORK_BITCOIN
    )

    with pytest.raises(ValidationError) as error:
        addr.full_clean()

    assert (
        "Invalid address for the given network" in error.value.message_dict["__all__"]
    )


def test_address_is_unique():
    mommy.make(Address, address=VALID_MONERO_MAINNET_ADDR)

    with pytest.raises(IntegrityError):
        mommy.make(Address, address=VALID_MONERO_MAINNET_ADDR)
