from django.conf import settings
from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes

import Backend.utils as utils

from custom_auth.utils import (
    ApiErrorsMixin,
    PublicApiMixin,
    AuthApiMixin,
    add_auth_cookies,
)
from custom_auth.authentication import CookieJWTAuthentication


class LoginCheck(APIView, PublicApiMixin, ApiErrorsMixin):
    def get(self, request):
        # TODO: add data
        print("!!! Start LoginCheck")
        # print("!!! request.COOKIES=", request.COOKIES)
        # print("!!! request.headers=", request.headers)
        if not request.user.is_authenticated:
            return Response(
                {"is_authenticated": False},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "is_authenticated": True,
                "user": {
                    "email": request.user.email,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )


class AuthTokenRefreshApiView(CookieJWTAuthentication, TokenRefreshView):
    # TODO: @extended_schema
    # TODO: enforce csrf
    def post(self, request: Request, *args, **kwargs):
        current_refresh_token = (
            request.COOKIES.get(settings.SIMPLE_JWT["AUTH_REFRESH_TOKEN"])
            or None
        )
        current_acces_token = (
            request.COOKIES.get(settings.SIMPLE_JWT["AUTH_ACCESS_TOKEN"])
            or None
        )
        current_tokens = {
            "access": current_acces_token,
            "refresh": current_refresh_token,
        }

        # Uses TOKEN_REFRESH_SERIALIZER that handles tokens rotation and update
        updated_tokens = utils.validate_data(
            current_tokens,
            self.get_serializer_class(),
            verbose_code="refresh_token_validaion_failed",
        )

        # TODO: return RefreshToken living time or send it in /auth/user/info
        response = Response(status=status.HTTP_204_NO_CONTENT)
        add_auth_cookies(response, updated_tokens)

        return response


class LogoutApiView(AuthApiMixin, ApiErrorsMixin, APIView):
    def post(self, request):
        # user_change_secret_key(user=request.user)

        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_ACCESS_TOKEN"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_REFRESH_TOKEN"])

        return response
