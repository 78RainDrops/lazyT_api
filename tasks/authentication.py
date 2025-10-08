from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework import exceptions, status
from django.contrib.auth.models import User
from .utils import verify_user


class CustomeAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        user = verify_user(token)

        if not user:
            raise exceptions.AuthenticationFailed("Invalid or expired token")

        return (user, token)
