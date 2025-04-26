from django.conf import settings
from django.http import HttpResponse
# from django.middleware import csrf # TODO
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework import exceptions as rest_exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from custom_auth.authentication import CookieJWTAuthentication
from users.models import User


class AuthApiMixin:
    authentication_classes = (CookieJWTAuthentication, )
    # authentication_classes = ()
    # permission_classes = (IsAuthenticated, ) # TODO: fix
    permission_classes = ()


class PublicApiMixin:
    authentication_classes = ()
    permission_classes = ()


class ApiErrorsMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    Without the mixin, they return 500 status code which is not desired.
    """
    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
        User.DoesNotExist: rest_exceptions.NotAuthenticated
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)


def _get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    print(f"refresh.token_type={refresh.token_type}")
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# TODO: remove ??? All logic is inside login_or_refresh_by_cookies_django
def login_or_refresh_by_cookies(user, response: Response) -> Response:
    if not user.is_active:
        return Response(
            {"error": "This account is not active"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # login(request, user) # TODO: not needed with custom authentication ???

    data = _get_tokens_for_user(user)
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN'],
        value=data["access"],
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_REFRESH_TOKEN'],
        value=data["refresh"],
        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    # TODO: add refresh token !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # csrf.get_token(request) # TODO

    # email_template = render_to_string(
    #     'login_success.html',
    #     {"username":user.username}
    # )
    # login = EmailMultiAlternatives(
    #     "Successfully Login",
    #     "Successfully Login",
    #     settings.EMAIL_HOST_USER,
    #     [user.email],
    # )
    # login.attach_alternative(email_template, 'text/html')
    # login.send()

    # response.data = {
    #     "Success" : "Login successfully",
    #     "data": data,
    # }

    return response


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def login_or_refresh_by_cookies_django(user, response: HttpResponse) -> HttpResponse:
    """Similar to login_or_refresh_by_cookies but works with Django's HttpResponse"""
    if not user.is_active:
        return HttpResponse(
            "This account is not active",
            status=404
        )

    data = _get_tokens_for_user(user)
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN'],
        value=data["access"],
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_REFRESH_TOKEN'],
        value=data["refresh"],
        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )

    return response


def get_error_message(exc) -> str:
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg
