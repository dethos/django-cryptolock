=============================
Django-Cryptolock
=============================

.. image:: https://badge.fury.io/py/django-cryptolock.svg
    :target: https://badge.fury.io/py/django-cryptolock

.. image:: https://travis-ci.org/dethos/django-cryptolock.svg?branch=master
    :target: https://travis-ci.org/dethos/django-cryptolock

.. image:: https://coveralls.io/repos/github/dethos/django-cryptolock/badge.svg
    :target: https://coveralls.io/github/dethos/django-cryptolock

Authentication using cryptocurrency wallets for Django projects.

This package provides a django app containing a set of utilities to
implement the BitId and Monero Cryptolock authentication "protocols".

Future releases might include other cryptocurrencies but for the being
(until we reach some stability) all the focus will remain on BTC and XMR.

**DISCLAIMER:** This package is on a early stage of development, It isn't meant to be
used on production (in other words, only test projects for now).

Documentation
-------------

The full documentation is at https://django-cryptolock.readthedocs.io.

Quickstart
----------

1. Install Django-Cryptolock::

    pip install django-cryptolock

2. Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "django_cryptolock.apps.DjangoCryptolockConfig",
        ...
    )

3. Migrate your database::

    python manage.py migrate


4. Add the following settings to your project for the Monero Backend:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
        "django_cryptolock.backends.MoneroAddressBackend",
        ...
    ]
    DJCL_MONERO_NETWORK = "mainnet"
    DJCL_MONERO_WALLET_RPC_PROTOCOL = "<http_or_https>"
    DJCL_MONERO_WALLET_RPC_HOST = "<wallet_rpc_host>:<port>"
    DJCL_MONERO_WALLET_RPC_USER = "<user>"
    DJCL_MONERO_WALLET_RPC_PASS = "<password>"

5. Add Django-Cryptolock's URL patterns:

.. code-block:: python

    from django.conf.urls import url


    urlpatterns = [
        ...
        url(r"^auth/", include("django_cryptolock.urls", namespace="django_cryptolock")),
        ...
    ]

More detailed information can be found in the [documentation](#documentation).
