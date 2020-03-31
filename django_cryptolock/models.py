# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from model_utils.models import TimeStampedModel

from .validators import validate_monero_address, validate_bitcoin_address


class Address(TimeStampedModel):
    """Addresses that belong to a given user account."""

    NETWORK_MONERO = 1
    NETWORK_BITCOIN = 2

    NETWORKS = ((NETWORK_MONERO, "Monero"), (NETWORK_BITCOIN, "Bitcoin"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    network = models.PositiveSmallIntegerField(choices=NETWORKS, default=NETWORK_MONERO)
    address = models.CharField(max_length=106, unique=True)

    class Meta:
        """Meta definition for Address."""

        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        """Unicode representation of Address."""
        return self.address

    def clean(self):
        try:
            if self.network == self.NETWORK_MONERO:
                validate_monero_address(self.address)
            else:
                validate_bitcoin_address(self.address)
        except ValidationError:
            raise ValidationError(_("Invalid address for the given network"))
