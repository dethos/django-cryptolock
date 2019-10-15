from django.contrib.auth.backends import ModelBackend


class MoneroAddressBackend(ModelBackend):
    def authenticate(self, request, address=None, challenge=None, signature=None):
        pass
