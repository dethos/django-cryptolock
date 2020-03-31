from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from pybitid import bitid

from .models import Address
from .validators import validate_monero_address, validate_bitcoin_address
from .utils import generate_challenge


class ChallengeMixin(forms.Form):
    """
    Used on authentication forms to make sure an unique challenge is included.

    This mixin ensures that the challenge is always controlled by the server.
    """

    challenge = forms.CharField()

    def include_challange(self):
        new_challenge = bitid.build_uri(
            self.request.build_absolute_uri(), generate_challenge()
        )
        if not self.data:
            self.request.session["current_challenge"] = new_challenge
            self.initial["challenge"] = new_challenge

    def clean_challenge(self):
        challenge = self.cleaned_data.get("challenge")
        if not challenge or challenge != self.request.session.get("current_challenge"):
            raise forms.ValidationError(_("Invalid or outdated challenge"))

        return challenge


class SimpleLoginForm(ChallengeMixin, forms.Form):
    """Basic login form, that can be used as reference for implementation."""

    address = forms.CharField()
    signature = forms.CharField()

    error_messages = {
        "invalid_login": _("Please enter a correct Monero address or signature."),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """When rendering the form (no data provided) a new challenge
        must be created."""
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None
        self.include_challange()

    def clean(self):
        address = self.cleaned_data.get("address")
        challenge = self.cleaned_data.get("challenge")
        signature = self.cleaned_data.get("signature")

        if address and challenge and signature:
            self.user_cache = authenticate(
                self.request, address=address, challenge=challenge, signature=signature
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"], code="inactive"
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages["invalid_login"], code="invalid_login"
        )


class SimpleSignUpForm(ChallengeMixin, forms.Form):
    """Basic login form, that can be used as reference for implementation."""

    username = forms.CharField()
    address = forms.CharField()
    signature = forms.CharField()

    def __init__(self, request=None, *args, **kwargs):
        """When rendering the form (no data provided) a new challenge
        must be created."""
        super().__init__(*args, **kwargs)
        self.request = request
        self.include_challange()
        self.network = None

    def clean_address(self):
        self.network = None
        value = self.cleaned_data["address"]
        bitcoin_backend = "django_cryptolock.backends.BitcoinAddressBackend"
        monero_backend = "django_cryptolock.backends.MoneroAddressBackend"

        if bitcoin_backend in settings.AUTHENTICATION_BACKENDS:
            try:
                validate_bitcoin_address(value)
                self.network = Address.NETWORK_BITCOIN
            except ValidationError:
                pass

        if monero_backend in settings.AUTHENTICATION_BACKENDS:
            try:
                validate_monero_address(value)
                self.network = Address.NETWORK_MONERO
            except ValidationError:
                pass

        if not self.network:
            raise forms.ValidationError(_("Invalid address"))

        if Address.objects.filter(address=value).exists():
            raise forms.ValidationError(_("This address already exists"))

        return value

    def clean_username(self):
        value = self.cleaned_data["username"]
        if get_user_model().objects.filter(username=value).exists():
            raise forms.ValidationError(_("This username is already taken"))
        return value
