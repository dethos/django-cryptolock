# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import MoneroLoginView, MoneroSignUpView


app_name = "django_cryptolock"
urlpatterns = [
    url(r"login", MoneroLoginView.as_view(), name="login"),
    url(r"signup", MoneroSignUpView.as_view(), name="signup"),
]
