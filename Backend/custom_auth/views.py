from django.conf import settings
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

import Backend.utils as utils
from custom_auth.authentication import CookieJWTAuthentication
from custom_auth.cookies import add_auth_cookies
from custom_auth.csrf import enforce_csrf
from custom_auth.serializers import AuthUserInfoResponseSerializer
from custom_auth.utils import get_auth_user_info


class AuthUserInfoApiView(APIView):
    @extend_schema(
        responses={
            status.HTTP_200_OK: AuthUserInfoResponseSerializer,
        },
    )
    def get(self, request: Request):
        return get_auth_user_info(request)


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
            request.COOKIES.get(settings.SIMPLE_JWT["AUTH_REFRESH_TOKEN"]) or None
        )
        current_acces_token = (
            request.COOKIES.get(settings.SIMPLE_JWT["AUTH_ACCESS_TOKEN"]) or None
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

        # Authenticate user
        request.COOKIES[settings.SIMPLE_JWT["AUTH_ACCESS_TOKEN"]] = updated_tokens[
            "access"
        ]
        request.COOKIES[settings.SIMPLE_JWT["AUTH_REFRESH_TOKEN"]] = updated_tokens[
            "refresh"
        ]
        user, _ = self.authenticate(request)
        request.user = user

        response = get_auth_user_info(request)
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
