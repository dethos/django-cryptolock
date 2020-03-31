from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

from monerorpc.authproxy import JSONRPCException

from .models import Address
from .utils import verify_monero_signature, verify_bitcoin_signature


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
            is_valid = verify_monero_signature(
                stored_address.address, challenge, signature
            )
        except JSONRPCException:
            raise PermissionDenied(_("Error while validating signature"))

        if is_valid:
            return stored_address.user

        return None


class BitcoinAddressBackend(ModelBackend):
    """Custom Bitcoin-BitId authentication backend."""

    def authenticate(
        self, request, address=None, challenge=None, signature=None, **kwargs
    ):
        """
        Validates the provided signature for the given Bitcoin address and challenge.

        This method does not rely on any external components, everything is done locally.
        """
        if not all([address, challenge, signature]):
            return None

        stored_address = (
            Address.objects.select_related("user")
            .filter(address=address, network=Address.NETWORK_BITCOIN)
            .first()
        )
        if not stored_address:
            return None

        valid_signature = verify_bitcoin_signature(
            stored_address.address, challenge, signature, request
        )

        if valid_signature:
            return stored_address.user
        else:
            return None
