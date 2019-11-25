import pytest
from model_mommy import mommy

from django_cryptolock.utils import generate_challenge


def test_challenge_has_8_bytes():
    challenge = generate_challenge()
    assert len(bytes.fromhex(challenge)) == 8
