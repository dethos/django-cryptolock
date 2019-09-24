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

Add Django-Cryptolock's URL patterns:

.. code-block:: python

    from django_cryptolock import urls as django_cryptolock_urls


    urlpatterns = [
        ...
        url(r'^', include(django_cryptolock_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
