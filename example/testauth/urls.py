from django.conf.urls import url

from .views import TestLoginView, TestSignupView

urlpatterns = [
    url(r"login", TestLoginView.as_view(), name="test_login"),
    url(r"signup", TestSignupView.as_view(), name="test_signup"),
]
