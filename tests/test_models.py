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

pytestmark = pytest.mark.django_db


def test_valid_mainnet_address(settings):
    settings.DJCL_MONERO_NETWORK = "mainnet"

    addr = mommy.make(Address, address=VALID_MONERO_MAINNET_ADDR)
    addr.full_clean()


def test_valid_stagenet_addr(settings):
    settings.DJCL_MONERO_NETWORK = "stagenet"

    addr = mommy.make(Address, address=VALID_MONERO_STAGENET_ADDR)
    addr.full_clean()


def test_valid_testnet_addr(settings):
    settings.DJCL_MONERO_NETWORK = "testnet"

    addr = mommy.make(Address, address=VALID_MONERO_TESTNET_ADDR)
    addr.full_clean()


def test_invalid_address():
    bad_addr = "Verywrongaddress"
    addr = mommy.make(Address, address=bad_addr)

    with pytest.raises(ValidationError) as error:
        addr.full_clean()

    assert f"{bad_addr} is not a valid address" in error.value.message_dict["address"]


def test_wrong_network_address(settings):
    settings.DJCL_MONERO_NETWORK = "stagenet"
    addr = mommy.make(Address, address=VALID_MONERO_MAINNET_ADDR)

    with pytest.raises(ValidationError) as error:
        addr.full_clean()

    assert "Invalid address for stagenet" in error.value.message_dict["address"]


def test_address_is_unique():
    addr = mommy.make(Address, address=VALID_MONERO_MAINNET_ADDR)

    with pytest.raises(IntegrityError):
        mommy.make(Address, address=VALID_MONERO_MAINNET_ADDR)
