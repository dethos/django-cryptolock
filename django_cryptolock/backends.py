from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

from .models import Address
from .utils import verify_signature

User = get_user_model()


class MoneroAddressBackend(ModelBackend):
    """Custom Monero-Cryptolock authentication backend."""

    def authenticate(self, request, address=None, challenge=None, signature=None):
        """Validates the provided signature for the given address and challenge.

        This method currently relies on Wallet RPC access to verify the signature,
        in the future it should be done locally to be more reliable and more
        performant.
        """
        if not all([address, challenge, signature]):
            return None

        stored_address = (
            Address.objects.select_related("user").filter(address=address).first()
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
