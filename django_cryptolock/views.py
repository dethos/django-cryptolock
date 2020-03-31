# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.forms.utils import ErrorList
from django.conf import settings

from monerorpc.authproxy import JSONRPCException

from .forms import SimpleSignUpForm, SimpleLoginForm
from .utils import verify_monero_signature, verify_bitcoin_signature
from .models import Address


class CryptoLockLoginView(LoginView):
    template_name = "django_cryptolock/login.html"
    form_class = SimpleLoginForm


class CryptoLockSignUpView(FormView):
    template_name = "django_cryptolock/signup.html"
    form_class = SimpleSignUpForm

    def get_form(self, form_class=None):
        return self.form_class(request=self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        try:
            valid_sig = self.verify_signature(form)
        except JSONRPCException:
            form._errors["__all__"] = ErrorList(
                [_("Error connecting to Monero daemon")]
            )
            return self.form_invalid(form)

        username = form.cleaned_data["username"]
        address = form.cleaned_data["address"]

        if valid_sig:
            user = get_user_model().objects.create(username=username)
            user.address_set.create(address=address, network=form.network)
            return super().form_valid(form)
        else:
            form._errors["signature"] = ErrorList([_("Invalid signature")])
            return self.form_invalid(form)

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL

    def verify_signature(self, form):
        address = form.cleaned_data["address"]
        challenge = form.cleaned_data["challenge"]
        signature = form.cleaned_data["signature"]
        bitcoin = form.network == Address.NETWORK_BITCOIN
        monero = form.network == Address.NETWORK_MONERO
        valid_sig = False

        if bitcoin:
            valid_sig = verify_bitcoin_signature(
                address, challenge, signature, request=self.request
            )
        elif monero:
            valid_sig = verify_monero_signature(address, challenge, signature)

        return valid_sig
