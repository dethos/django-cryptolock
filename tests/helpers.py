"""
Set of functions and constants that help testing the existing functionality
"""


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
