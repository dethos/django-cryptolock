import warnings
from typing import Union
from secrets import token_hex

from django.conf import settings
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from monerorpc.authproxy import AuthServiceProxy
from pybitid import bitid


def verify_monero_signature(address: str, challenge: str, signature: str) -> bool:
    """Makes a request to wallet RPC to verify address and signature."""
    protocol = settings.DJCL_MONERO_WALLET_RPC_PROTOCOL
    host = settings.DJCL_MONERO_WALLET_RPC_HOST
    user = settings.DJCL_MONERO_WALLET_RPC_USER
    pwd = settings.DJCL_MONERO_WALLET_RPC_PASS
    wallet_rpc = AuthServiceProxy(f"{protocol}://{user}:{pwd}@{host}/json_rpc")

    result = wallet_rpc.verify(
        {"data": challenge, "address": address, "signature": signature}
    )

    return result.get("good", False)


def verify_bitcoin_signature(
    address: str, challenge: str, signature: str, request: HttpRequest
) -> bool:
    """Verifies if the provided bitcoin signature is valid."""
    network = getattr(settings, "DJCL_BITCOIN_NETWORK", None)
    if not network:
        warnings.warn(_("Please configure the bitcoin network in the settings file"))
    is_testnet = True if network == "testnet" else False
    callback_uri = request.build_absolute_uri()
    return bitid.challenge_valid(
        address, signature, challenge, callback_uri, is_testnet
    )


def verify_signature(
    network: str, address: str, challenge: str, signature: str, request: HttpRequest
):
    valid_sig = False

    if network == "Bitcoin":
        valid_sig = verify_bitcoin_signature(
            address, challenge, signature, request=request
        )
    elif network == "Monero":
        valid_sig = verify_monero_signature(address, challenge, signature)

    return valid_sig


def generate_challenge():
    """Generates a new random challenge for the authentication."""
    num_bytes = getattr(settings, "DJCL_CHALLENGE_BYTES", 16)
    return token_hex(num_bytes)
