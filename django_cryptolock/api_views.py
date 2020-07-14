from django.utils.translation import gettext_lazy as _
from rest_framework.status import HTTP_200_OK

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from monerorpc.authproxy import JSONRPCException

from .models import Address, Challenge
from .forms import SimpleSignUpForm, SimpleLoginForm
from .utils import verify_signature
from .mixins import CreateUserMixin, CreateChallengeMixin


class CryptoLockAPITokenLoginView(CreateChallengeMixin, APIView):
    """Endpoint to login the user with cryptocurrency wallet address.

    Using the default token backend.
    """

    http_method_names = ["get", "post"]

    def post(self, request, format=None):
        """Authenticates the user using the provided signature."""
        form = SimpleLoginForm(request, request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        challenge = form.cleaned_data["challenge"]
        Challenge.objects.invalidate(challenge)
        Challenge.objects.clean_expired()

        token = Token.objects.create(user=form.user_cache)
        return Response({"token": token.key}, status=HTTP_200_OK)


class CryptoLockAPISignUpView(CreateUserMixin, CreateChallengeMixin, APIView):
    """Endpoint to create a new user using cryptocurrency wallet address."""

    http_method_names = ["get", "post"]

    def post(self, request, format=None):
        """Verifies the signature and creates a new user account."""
        form = SimpleSignUpForm(request, request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        username = form.cleaned_data["username"]
        address = form.cleaned_data["address"]
        challenge = form.cleaned_data["challenge"]
        signature = form.cleaned_data["signature"]
        network = [n[1] for n in Address.NETWORKS if n[0] == form.network][0]

        try:
            valid_sig = verify_signature(
                network, address, challenge, signature, self.request
            )
        except JSONRPCException:
            return Response(
                {"__all__": [_("Error connecting to Monero daemon")]},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if valid_sig:
            self.create_user(username, challenge, address, form.network)
            return Response({}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"signature": [_("Invalid signature")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
