"""
Set of functions and constants that help testing the existing functionality
"""
from pybitid import bitid

from django_cryptolock.models import Challenge

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


def gen_challenge():
    return bitid.build_uri(EXAMPLE_LOGIN_URL, Challenge.objects.generate())
