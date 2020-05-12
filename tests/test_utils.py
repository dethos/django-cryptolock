import pytest
from model_mommy import mommy

from django_cryptolock.utils import generate_challenge


def test_challenge_has_default_byte_len():
    challenge = generate_challenge()
    assert len(bytes.fromhex(challenge)) == 16


@pytest.mark.parametrize("length", (8, 16, 32, 64))
def test_challenge_has_custom_byte_len(length, settings):
    settings.DJCL_CHALLENGE_BYTES = length
    challenge = generate_challenge()
    assert len(bytes.fromhex(challenge)) == length
