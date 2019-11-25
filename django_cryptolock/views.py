# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.forms.utils import ErrorList
from django.conf import settings
from django.urls import reverse

from monerorpc.authproxy import JSONRPCException

from .forms import SimpleSignUpForm, SimpleLoginForm
from .utils import verify_signature


class MoneroLoginView(LoginView):
    form_class = SimpleLoginForm


class MoneroSignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = SimpleSignUpForm

    def get_form(self, form_class=None):
        return self.form_class(request=self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        address = form.cleaned_data["address"]
        challenge = form.cleaned_data["challenge"]
        signature = form.cleaned_data["signature"]
        try:
            valid_sig = verify_signature(address, challenge, signature)
        except JSONRPCException:
            form._errors["__all__"] = ErrorList([_("Error connecting to daemon")])
            return self.form_invalid(form)

        if valid_sig:
            user = get_user_model().objects.create(username=username)
            user.address_set.create(address=address)
            return super().form_valid(form)
        else:
            form._errors["signature"] = ErrorList([_("Invalid signature")])
            return self.form_invalid(form)

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL
