# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'django_cryptolock'
urlpatterns = [
    url(
        regex="^Address/~create/$",
        view=views.AddressCreateView.as_view(),
        name='Address_create',
    ),
    url(
        regex="^Address/(?P<pk>\d+)/~delete/$",
        view=views.AddressDeleteView.as_view(),
        name='Address_delete',
    ),
    url(
        regex="^Address/(?P<pk>\d+)/$",
        view=views.AddressDetailView.as_view(),
        name='Address_detail',
    ),
    url(
        regex="^Address/(?P<pk>\d+)/~update/$",
        view=views.AddressUpdateView.as_view(),
        name='Address_update',
    ),
    url(
        regex="^Address/$",
        view=views.AddressListView.as_view(),
        name='Address_list',
    ),
	]
