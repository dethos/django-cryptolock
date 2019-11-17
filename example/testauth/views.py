from django.shortcuts import render
from django_cryptolock.views import MoneroLoginView, MoneroSignUpView


class TestLoginView(MoneroLoginView):
    pass


class TestSignupView(MoneroSignUpView):
    pass
