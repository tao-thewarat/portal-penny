import hmac

from django.conf import settings
from rest_framework.permissions import BasePermission


class HasBotApiToken(BasePermission):
    """
    Lets the Penny Discord bot write transactions without a browser session.

    The bot sends `Authorization: Bearer <PENNY_API_TOKEN>`. An unset token on
    the server denies every request rather than opening the endpoint, and the
    comparison is constant-time so the token cannot be guessed byte by byte.
    """

    message = "Missing or invalid API token."

    def has_permission(self, request, view):
        expected = settings.PENNY_API_TOKEN
        if not expected:
            return False

        scheme, _, provided = request.headers.get("Authorization", "").partition(" ")
        if scheme.lower() != "bearer" or not provided:
            return False

        return hmac.compare_digest(provided.encode(), expected.encode())
