# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "!z^^097u*@)yq#w1n14m%uh-l67#h&uft9p+m%$$(0y(s%-q7o"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_cryptolock",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()

AUTHENTICATION_BACKENDS = [
    "django_cryptolock.backends.MoneroAddressBackend",
    "django_cryptolock.backends.BitcoinAddressBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Test only default settings
DJCL_MONERO_NETWORK = "stagenet"
DJCL_BITCOIN_NETWORK = "mainnet"

DJCL_MONERO_WALLET_RPC_HOST = "localhost:3030"
DJCL_MONERO_WALLET_RPC_USER = "test"
DJCL_MONERO_WALLET_RPC_PASS = "test"
DJCL_MONERO_WALLET_RPC_PROTOCOL = "http"
