from django.core.exceptions import ValidationError

import pytest

from django_cryptolock.validators import validate_monero_address


@pytest.mark.parametrize(
    "network,address",
    [
        (
            "mainnet",
            "46fYuhPAdsxMbEeMg97LhSbFPamdiCw7C6b19VEcZSmV6xboWFZuZQ9MTbj1wLszhUExHi63CMtsWjDTrRDqegZiPVebgYq",
        ),
        (
            "stagenet",
            "5A2uBqpNg7E4cYzA7bhXeuP9C2qSeUAtDhUScFgTBJWMUNJd9yZJxwDHg8sPVPBBx7JJFYqxDSbb7HFz2w8dttVJKW5Yipp",
        ),
        (
            "testnet",
            "9waU7xxRYbC2HkKV2k4dzPjEYwkYDiHmfELLUkS8vegVLEYkk2dk3X5JJZtURNthsaDh8zL5SYAp8VXMzqvRYptgGTYNpEn",
        ),
    ],
)
def test_valid_address(network, address, settings):
    settings.DJCL_MONERO_NETWORK = network
    assert validate_monero_address(address) is None


@pytest.mark.parametrize(
    "network,address",
    [
        (
            "mainnet",
            "9waU7xxRYbC2HkKV2k4dzPjEYwkYDiHmfELLUkS8vegVLEYkk2dk3X5JJZtURNthsaDh8zL5SYAp8VXMzqvRYptgGTYNpEn",
        ),
        (
            "stagenet",
            "46fYuhPAdsxMbEeMg97LhSbFPamdiCw7C6b19VEcZSmV6xboWFZuZQ9MTbj1wLszhUExHi63CMtsWjDTrRDqegZiPVebgYq",
        ),
        (
            "testnet",
            "5A2uBqpNg7E4cYzA7bhXeuP9C2qSeUAtDhUScFgTBJWMUNJd9yZJxwDHg8sPVPBBx7JJFYqxDSbb7HFz2w8dttVJKW5Yipp",
        ),
    ],
)
def test_invalid_address(network, address, settings):
    settings.DJCL_MONERO_NETWORK = network

    with pytest.raises(ValidationError) as error:
        validate_monero_address(address)

    assert f"Invalid address for {network}" in str(error.value)
