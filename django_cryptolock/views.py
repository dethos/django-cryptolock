# -*- coding: utf-8 -*-
from django.contrib.auth.views import LoginView
from django.views.generic import FormView

from .forms import SimpleSignUpForm


class MoneroLoginView(LoginView):
    pass


class MoneroSignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = SimpleSignUpForm
