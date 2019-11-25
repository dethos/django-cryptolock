from secrets import token_hex

from django.conf import settings

from monerorpc.authproxy import AuthServiceProxy


def verify_signature(address: str, challenge: str, signature: str) -> bool:
    """Makes a request to wallet RPC to verify address and signature."""
    protocol = settings.MONERO_WALLET_RPC_PROTOCOL
    host = settings.MONERO_WALLET_RPC_HOST
    user = settings.MONERO_WALLET_RPC_USER
    pwd = settings.MONERO_WALLET_RPC_PASS
    wallet_rpc = AuthServiceProxy(f"{protocol}://{user}:{pwd}@{host}/json_rpc")

    result = wallet_rpc.verify(
        {"data": challenge, "address": address, "signature": signature}
    )

    return result.get("good", False)


def generate_challenge():
    """Generates a new random challenge for the authentication."""
    return token_hex(8)
