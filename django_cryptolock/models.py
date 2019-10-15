# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from .validators import validate_monero_address


class Address(TimeStampedModel):
    """Addresses that belong to a given user account."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(
        max_length=106, validators=[validate_monero_address], unique=True
    )

    class Meta:
        """Meta definition for Address."""

        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        """Unicode representation of Address."""
        return self.address
