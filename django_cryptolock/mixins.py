from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status

from pybitid import bitid

from .models import Challenge
from .serializers import ChallengeSerializer


class CreateChallengeMixin:
    """Add create challenge on get functionality to API views."""

    def get(self, request, format=None):
        """Returns a new challenge for the login."""
        serializer = ChallengeSerializer(instance=Challenge.objects.generate())
        serializer.data["challenge"] = bitid.build_uri(
            request.build_absolute_uri(), serializer.data["challenge"]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserMixin:
    @transaction.atomic
    def create_user(self, username, challenge, address, network):
        user = get_user_model().objects.create(username=username)
        user.address_set.create(address=address, network=network)
        Challenge.objects.invalidate(challenge)
