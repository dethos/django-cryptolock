# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	Address,
)


class AddressCreateView(CreateView):

    model = Address


class AddressDeleteView(DeleteView):

    model = Address


class AddressDetailView(DetailView):

    model = Address


class AddressUpdateView(UpdateView):

    model = Address


class AddressListView(ListView):

    model = Address

