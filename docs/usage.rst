=====
Usage
=====

To use Django-Cryptolock in a project, add it to your `INSTALLED_APPS`:

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
