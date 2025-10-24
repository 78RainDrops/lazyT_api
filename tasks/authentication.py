from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .utils import verify_user


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        # missing authorization header
        if not auth_header:
            return None

        # invalid header format
        if not auth_header.startswith("Bearer "):
            raise exceptions.AuthenticationFailed("Invalid token header")

        # extract token
        token = auth_header.split(" ")[1]
        # verify user
        user = verify_user(token)

        if not user:
            raise exceptions.AuthenticationFailed("Invalid or expired token")

        return (user, token)
