from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        validated = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated)

        if not user.is_active:
            return None

        return user


jwt_auth = JWTBearer()
