# -*- coding: utf-8 -*-
from django.contrib.auth.views import LoginView
from django.views.generic import FormView

from .models import Address


class MoneroLoginView(LoginView):
    pass


class MoneroSignUpView(FormView):
    pass
