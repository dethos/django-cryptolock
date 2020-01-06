=============================
Django-Cryptolock
=============================

.. image:: https://badge.fury.io/py/django-cryptolock.svg
    :target: https://badge.fury.io/py/django-cryptolock

.. image:: https://travis-ci.org/dethos/django-cryptolock.svg?branch=master
    :target: https://travis-ci.org/dethos/django-cryptolock

.. image:: https://coveralls.io/repos/github/dethos/django-cryptolock/badge.svg
    :target: https://coveralls.io/github/dethos/django-cryptolock

Django authentication using cryptocurrency wallets

Documentation
-------------

The full documentation is at https://django-cryptolock.readthedocs.io.

Quickstart
----------

Install Django-Cryptolock::

    pip install django-cryptolock

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_cryptolock.apps.DjangoCryptolockConfig',
        ...
    )

Migrate your database.

Add Django-Cryptolock's URL patterns:

.. code-block:: python

    from django.conf.urls import url


    urlpatterns = [
        ...
        url(r"^auth/", include("django_cryptolock.urls", namespace="django_cryptolock")),
        ...
    ]


Add the following settings to your project:

* ``django_cryptolock.backends.MoneroAddressBackend`` to your
  ``AUTHENTICATION_BACKENDS``
* Set ``DJCL_MONERO_NETWORK`` with the network in use: ``mainnet``,
  ``stagenet`` or ``testnet``
* Use ``DJCL_MONERO_WALLET_RPC_PROTOCOL``, ``DJCL_MONERO_WALLET_RPC_HOST``,
  ``DJCL_MONERO_WALLET_RPC_USER`` and ``DJCL_MONERO_WALLET_RPC_PASS`` to specify
  which wallet RPC should be used.

Finaly create the templates files (``login.html`` and ``signup.html``) under a
``django_cryptolock`` subfolder.

Features
--------

* Adds authentication based on cryptocurrency wallets to a Django project.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox -e <your-python-version>-django-22

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
