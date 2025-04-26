from django.contrib import auth
from django.conf import settings

from django.utils.deprecation import MiddlewareMixin

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import CSRFCheck

from rest_framework import exceptions


def generate_jwt_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    print(f"!!! generate_tokens_for_user")
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def update_jwt_tokens():
    print(f"!!! update_jwt_tokens")
    pass


def enforce_csrf(request):
    """
    Enforce CSRF validation.
    """
    check = CSRFCheck(request) # TODO: verify !!!
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied(f'CSRF check failed: {reason}')


class CookieJWTAuthentication(JWTAuthentication):
    # TODO: enforce csrf decorator
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN']) or None
        else:
            # Fallback to get token from headers instead of cookie
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        # enforce_csrf(request)
        return self.get_user(validated_token), validated_token
