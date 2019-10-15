from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from monero.address import Address


def validate_monero_address(value):
    try:
        address = Address(value)
    except ValueError as e:
        raise ValidationError(
            _("%(value)s is not a valid address"), params={"value": value}
        )

    network = getattr(settings, "DJCL_MONERO_NETWORK", None)
    if not network:
        raise ValidationError(
            _("Please configure the monero network in the settings file")
        )
    if network == "mainnet" and not address.is_mainnet():
        raise ValidationError(_("Invalid address for mainnet"))
    elif network == "stagenet" and not address.is_stagenet():
        raise ValidationError(_("Invalid address for stagenet"))
    elif network == "testnet" and not address.is_testnet():
        raise ValidationError(_("Invalid address for testnet"))
