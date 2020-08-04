from rest_framework import serializers

from .models import Challenge
from .forms import SimpleSignUpForm


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ["challenge", "expires"]
