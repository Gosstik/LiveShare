from functools import wraps

from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck


def enforce_csrf(func):
    """
    Decorator to enforce CSRF check
    """

    @wraps(func)
    def wrapped_view(request, *args, **kwargs):
        check = CSRFCheck(request)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f"CSRF check failed: {reason}")
        return func(request, *args, **kwargs)

    return wrapped_view
