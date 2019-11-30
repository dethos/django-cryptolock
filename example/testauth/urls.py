from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import IndexView

urlpatterns = [
    url(r"^logout$", LogoutView.as_view(), name="logout"),
    url(r"^$", IndexView.as_view(), name="index"),
]
