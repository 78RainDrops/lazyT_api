from django.conf import settings
import jwt
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User

ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token):
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def verify_user(token):
    payload = decode_token(token)

    if not payload:
        return None

    try:
        user = User.objects.get(id=payload["user_id"])
        return user
    except User.DoesNotExist:
        return None
