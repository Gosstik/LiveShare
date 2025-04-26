from django.contrib import auth
from django.conf import settings

from django.utils.deprecation import MiddlewareMixin

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions


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
    def authenticate(self, request):
        # TODO: remove or None
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN']) or None

        # header = self.get_header(request)

        # if header is None:
        #     raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN']) or None
        # else:
        #     raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        # enforce_csrf(request)
        return self.get_user(validated_token), validated_token


# TODO: remove
class CookieAuthenticationMiddleware(MiddlewareMixin):
    # List of paths that should skip authentication
    PUBLIC_PATHS = [
        '/auth/oauth/google/redirect',
        '/auth/oauth/google/callback',
    ]

    def process_request(self, request):
        # Skip authentication for public paths
        if request.path in self.PUBLIC_PATHS:
            return

        # Original implementation below
        # TODO: remove or None
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN']) or None
        if access_token is None:
            print("!!! access_token=None")
            # TODO: logout user --- need email
            return

        try:
            # TODO: replace JWTAuthentication with CookieJWTAuthentication ???
            jwt_object = JWTAuthentication()
            # TODO: skip ??? To manage 401
            validated_token = jwt_object.get_validated_token(access_token)
            print(f"validated_token={validated_token}")
            user = jwt_object.get_user(validated_token)
            print(type(user))
            print(f"user_email={user}")

            # id = request.COOKIES.get(user_cookie_name)
            # this will find the right backend
            # user = auth.authenticate(request)
            # print(type(user))
            # print(f"user={user}")
            # user = auth.authenticate(id)
            request.user = user
            # TODO: validate token
            request.is_access_token_expired = False
            # if you want to persist this user with Django cookie do the following
            #auth.login(request, user)
        except Exception:
            # If token validation fails, just return without setting user
            return
