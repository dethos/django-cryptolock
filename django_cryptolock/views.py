# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.forms.utils import ErrorList
from django.conf import settings

from monerorpc.authproxy import JSONRPCException

from .forms import SimpleSignUpForm, SimpleLoginForm
from .utils import verify_signature
from .models import Address, Challenge
from .mixins import CreateUserMixin


class CryptoLockLoginView(LoginView):
    template_name = "django_cryptolock/login.html"
    form_class = SimpleLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        challenge = form.cleaned_data["challenge"]
        Challenge.objects.invalidate(challenge)
        Challenge.objects.clean_expired()
        return response


class CryptoLockSignUpView(CreateUserMixin, FormView):
    template_name = "django_cryptolock/signup.html"
    form_class = SimpleSignUpForm

    def get_form(self, form_class=None):
        return self.form_class(request=self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        address = form.cleaned_data["address"]
        challenge = form.cleaned_data["challenge"]
        signature = form.cleaned_data["signature"]
        network = [n[1] for n in Address.NETWORKS if n[0] == form.network][0]

        try:
            valid_sig = verify_signature(
                network, address, challenge, signature, self.request
            )
        except JSONRPCException:
            form._errors["__all__"] = ErrorList(
                [_("Error connecting to Monero daemon")]
            )
            return self.form_invalid(form)

        if valid_sig:
            self.create_user(username, challenge, address, form.network)
            return super().form_valid(form)
        else:
            form._errors["signature"] = ErrorList([_("Invalid signature")])
            return self.form_invalid(form)

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL
