from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler


class JWTAuthentication(BaseJSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        _, token = auth_header.split()
        return token

    def authenticate(self, request):
        token = self.get_jwt_value(request)
        if token is None:
            return None

        try:
            payload = jwt_decode_handler(token)
            user = self.authenticate_credentials(payload)
            return (user, token)
        except Exception:
            raise AuthenticationFailed('Invalid token')
