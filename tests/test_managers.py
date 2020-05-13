from datetime import timedelta

from django.utils import timezone

import pytest
from model_mommy import mommy

from django_cryptolock.models import Challenge

pytestmark = pytest.mark.django_db


class TestChallengeManager:
    @pytest.mark.parametrize("conf", (None, 5, 10, 15, 20, 30, 60))
    def test_generate_challenge_with_expiration(self, settings, conf):
        if conf:
            settings.DJCL_CHALLENGE_EXPIRATION = conf
            test = timezone.now() + timedelta(minutes=conf + 1)
        else:
            test = timezone.now() + timedelta(minutes=11)

        assert not Challenge.objects.all().exists()

        challenge = Challenge.objects.generate()
        assert challenge.challenge
        assert challenge.expires < test
        assert Challenge.objects.all().exists()

    def test_is_active_when_expired(self):
        challenge = mommy.make(Challenge, challenge="1234", expires=timezone.now())
        assert not Challenge.objects.is_active(challenge=challenge.challenge)

    def test_is_active_when_inexistent(self):
        assert not Challenge.objects.is_active(challenge="1234")

    def test_is_active(self):
        challenge = Challenge.objects.generate()
        assert Challenge.objects.is_active(challenge=challenge.challenge)

    def test_invalidate_existing_challenge(self):
        challenge = Challenge.objects.generate()
        Challenge.objects.invalidate(challenge.challenge)
        assert not Challenge.objects.all().exists()

    def test_invalidate_inexistent_challenge(self):
        Challenge.objects.invalidate("1234")

    @pytest.mark.parametrize("num", (2, 5, 10, 15))
    def test_clean_expired_challenges(self, num):
        mommy.make(Challenge, num, expires=timezone.now())
        Challenge.objects.generate()
        deleted = Challenge.objects.clean_expired()
        assert deleted == num
        assert Challenge.objects.count() == 1
