from datetime import timedelta

from django.db.models.manager import Manager
from django.conf import settings
from django.utils import timezone

from .utils import generate_challenge


class ChallengeManager(Manager):
    """Provides methods to easily create and verify challenges."""

    def generate(self):
        token = generate_challenge()
        age = getattr(settings, "DJCL_CHALLENGE_EXPIRATION", 10)
        expiry_date = timezone.now() + timedelta(minutes=age)
        return self.create(challenge=token, expires=expiry_date)

    def is_active(self, challenge):
        """Returns True if the challenge can be used. Otherwise False."""
        now = timezone.now()
        return self.filter(challenge=challenge, expires__gte=now).exists()

    def invalidate(self, challenge):
        """Removes the provided challenge if it exists."""
        self.filter(challenge=challenge).delete()

    def clean_expired(self):
        """Delete all expired challenges. Returns nº of entries removed."""
        now = timezone.now()
        del_summary = self.filter(expires__lt=now).delete()
        return del_summary[0]
