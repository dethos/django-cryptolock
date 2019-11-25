from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from django_cryptolock.views import MoneroLoginView, MoneroSignUpView

urlpatterns = [
    url(r"login", MoneroLoginView.as_view(), name="test_login"),
    url(r"signup", MoneroSignUpView.as_view(), name="test_signup"),
    url(r"logout", LogoutView.as_view(), name="test_logout"),
]
