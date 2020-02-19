import warnings

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
from pybitid import bitid

from .models import Address
from .utils import verify_signature

User = get_user_model()


class MoneroAddressBackend(ModelBackend):
    """Custom Monero-Cryptolock authentication backend."""

    def authenticate(
        self, request, address=None, challenge=None, signature=None, **kwargs
    ):
        """Validates the provided signature for the given address and challenge.

        This method currently relies on Wallet RPC access to verify the signature,
        in the future it should be done locally to be more reliable and more
        performant.
        """
        if not all([address, challenge, signature]):
            return None

        stored_address = (
            Address.objects.select_related("user")
            .filter(address=address, network=Address.NETWORK_MONERO)
            .first()
        )
        if not stored_address:
            return None
        try:
            is_valid = verify_signature(address, challenge, signature)
        except JSONRPCException:
            raise PermissionDenied(_("Error while validating signature"))

        if is_valid:
            return stored_address.user

        return None


class BitcoinAddressBackend(ModelBackend):
    """Custom Bitcoin-BitId authentication backend."""

    def authenticate(
        self, request, address=None, bitid_uri=None, signature=None, **kwargs
    ):
        """
        Validates the provided signature for the given Bitcoin address and challenge.

        This method does not rely on any external components, everything is done locally.
        """
        network = getattr(settings, "DJCL_BITCOIN_NETWORK", None)
        if not network:
            warnings.warn(
                _("Please configure the bitcoin network in the settings file")
            )
        is_testnet = True if network == "testnet" else False

        if not all([address, bitid_uri, signature]):
            return None

        stored_address = (
            Address.objects.select_related("user")
            .filter(address=address, network=Address.NETWORK_BITCOIN)
            .first()
        )
        if not stored_address:
            return None

        callback_uri = request.build_absolute_uri()
        valid_signature = bitid.challenge_valid(
            address, signature, bitid_uri, callback_uri, is_testnet
        )

        if valid_signature:
            return stored_address.user
        else:
            return None
