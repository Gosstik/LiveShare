from django.conf import settings
from django.http import HttpResponse

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from Backend.exceptions import NotFound404

from users.models import User

def _generate_new_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def add_auth_cookies(response: HttpResponse | Response, tokens):
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN'],
        value=tokens["access"],
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_REFRESH_TOKEN'],
        value=tokens["refresh"],
        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )



def set_new_auth_cookies(user: User, response: HttpResponse) -> HttpResponse:
    if not user.is_active:
        raise NotFound404(
            code="account_is_not_active",
            detail=f"failed to set new auth tokens: account for user={user} is not active",
        )

    tokens = _generate_new_tokens_for_user(user)
    add_auth_cookies(response, tokens)

    return response
