import datetime as dt

from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.tokens import AccessToken

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
from users.serializers import UserResponseSerializer

from custom_auth.serializers import AuthUserInfoResponseSerializer

from custom_auth.utils import (
    ApiErrorsMixin,
    PublicApiMixin,
    AuthApiMixin,
)
from custom_auth.cookies import add_auth_cookies
from custom_auth.authentication import CookieJWTAuthentication
from custom_auth.csrf import enforce_csrf


class AuthUserInfoApiView(APIView):
    @extend_schema(
        responses={
            status.HTTP_200_OK: AuthUserInfoResponseSerializer,
        },
    )
    def get(self, request: Request):
        access_token_expiration = self._get_access_token_expiration_data(request)
        user_data = UserResponseSerializer(request.user).data
        response_data = {
            "access_token_expiration": access_token_expiration,
            "user": user_data,
        }

        return utils.validate_and_get_response(
            response_data,
            AuthUserInfoResponseSerializer,
        )

    def _get_access_token_expiration_data(self, request: Request):
        raw_access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN'])
        acccess_token = AccessToken(raw_access_token)
        exp_datetime = acccess_token['exp']

        exp_timestamp = dt.datetime.fromtimestamp(exp_datetime)
        left_datetime = exp_timestamp - dt.datetime.now()
        seconds_left = int(left_datetime.total_seconds())

        return {
            "seconds_left": seconds_left,
            "left_datetime": str(left_datetime),
            "expiration_timestamp": exp_timestamp.isoformat()
        }


class AuthTokenRefreshApiView(CookieJWTAuthentication, TokenRefreshView):
    @extend_schema(
        parameters=[],
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    @method_decorator(enforce_csrf)
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

        response = Response(status=status.HTTP_204_NO_CONTENT)
        add_auth_cookies(response, updated_tokens)

        return response


class AuthLogoutApiView(APIView):
    @extend_schema(
        parameters=[],
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_ACCESS_TOKEN"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_REFRESH_TOKEN"])

        return response
