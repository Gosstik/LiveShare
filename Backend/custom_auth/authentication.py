from django.conf import settings
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.authentication import JWTAuthentication

from custom_auth.csrf import enforce_csrf


class CookieJWTAuthentication(JWTAuthentication):
    @method_decorator(enforce_csrf)
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN'])
        else:
            # Fallback to get token from headers instead of cookie
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
