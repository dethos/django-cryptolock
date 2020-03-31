# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CryptoLockLoginView, CryptoLockSignUpView


app_name = "django_cryptolock"
urlpatterns = [
    url(r"login", CryptoLockLoginView.as_view(), name="login"),
    url(r"signup", CryptoLockSignUpView.as_view(), name="signup"),
]
