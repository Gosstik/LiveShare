from django.core.exceptions import ValidationError
from rest_framework import exceptions as rest_exceptions
from rest_framework.permissions import BasePermission, IsAuthenticated

from custom_auth.authentication import (
    CookieJWTAuthentication,
    OptionalCookieJWTAuthentication,
)
from users.models import User


class AuthApiMixin:
    authentication_classes = (CookieJWTAuthentication,)
    # authentication_classes = ()
    permission_classes = (IsAuthenticated,)  # TODO: fix
    # permission_classes = ()


class PublicApiMixin:
    authentication_classes = ()
    permission_classes = ()


class OptionalAuthApiMixin:
    authentication_classes = (OptionalCookieJWTAuthentication,)
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
        User.DoesNotExist: rest_exceptions.NotAuthenticated,
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(_get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)


class OptionalAuthForGetOnlyPermission(BasePermission):
    """
    Permission class that makes optional authentication for GET requests,
    but require authentication for other methods
    """

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user and request.user.is_authenticated


################################################################################

### Details


def _get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def _get_error_message(exc) -> str:
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    error_msg = _get_first_matching_attr(exc, "message", "messages")

    if isinstance(error_msg, list):
        error_msg = ", ".join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg
