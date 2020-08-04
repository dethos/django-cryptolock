# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.urls import path

from django_cryptolock.api_views import (
    CryptoLockAPITokenLoginView,
    CryptoLockAPISignUpView,
)


urlpatterns = [
    path(
        "api/token_login", CryptoLockAPITokenLoginView.as_view(), name="api_token_login"
    ),
    path("api/signup", CryptoLockAPISignUpView.as_view(), name="api_signup"),
    url(r"^", include("django_cryptolock.urls", namespace="django_cryptolock")),
]
