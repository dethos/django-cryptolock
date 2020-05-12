=====
Usage
=====

To use Django-Cryptolock in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "django_cryptolock.apps.DjangoCryptolockConfig",
        ...
    )

Now you should add the auth backend you wish to use on your project. You can use one or more:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
        "django_cryptolock.backends.BitcoinAddressBackend",
        "django_cryptolock.backends.MoneroAddressBackend",
    ]

Required Configuration
----------------------

If you use Monero, currently the following extra settings are required:

.. code-block:: python

    DJCL_MONERO_NETWORK = "mainnet"  # mainnet, stagenet or testnet
    DJCL_MONERO_WALLET_RPC_PROTOCOL = "<http_or_https>"
    DJCL_MONERO_WALLET_RPC_HOST = "<wallet_rpc_host>:<port>"
    DJCL_MONERO_WALLET_RPC_USER = "<user>"
    DJCL_MONERO_WALLET_RPC_PASS = "<password>"

For Bitcoin, you only need to set the ``DJCL_BITCOIN_NETWORK``:

.. code-block:: python

    DJCL_BITCOIN_NETWORK = "mainnet"  # mainnet or testnet

Optional Configuration
----------------------

``DJCL_CHALLENGE_BYTES`` can be used to customize the challenge length. The
default is ``16`` and you should avoid lower values unless you know what you
are doing.


Using the default forms and views
---------------------------------

Add Django-Cryptolock's URL patterns:

.. code-block:: python

    from django.conf.urls import url


    urlpatterns = [
        ...
        url(r"^auth/", include("django_cryptolock.urls", namespace="django_cryptolock")),
        ...
    ]

This will add 2 routes :

* ``django_cryptolock:signup``
* ``django_cryptolock:login``

You can then customize the generated HTML by creating the template files
(``login.html`` and ``signup.html``) under a ``django_cryptolock`` subfolder in
your templates directory.

Both of these templates will have access to a ``form`` containing the required
fields for the authentication.
