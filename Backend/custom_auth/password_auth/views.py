from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

import Backend.utils as utils
from Backend.exceptions import BadRequest400
from custom_auth.cookies import set_new_auth_cookies
from custom_auth.mixins import PublicApiMixin
from custom_auth.password_auth.serializers import (
    PasswordSigninRequestSerializer,
    PasswordSignupRequestSerializer,
)


class PasswordSignupApiView(PublicApiMixin, APIView):
    @extend_schema(
        request={
            "multipart/form-data": PasswordSignupRequestSerializer,
        },
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.Api4xxSerializer,
        },
    )
    def post(self, request):
        serializer = PasswordSignupRequestSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                response = Response(status=status.HTTP_204_NO_CONTENT)
                return set_new_auth_cookies(user, response)
        except serializers.ValidationError as e:
            if "email" in e.detail and "User with this email already exists" in str(
                e.detail["email"][0]
            ):
                raise BadRequest400(
                    code="email_already_exists",
                    detail="User with this email already exists",
                ) from e
            raise BadRequest400(detail=e.detail) from e


class PasswordSigninApiView(PublicApiMixin, APIView):
    @extend_schema(
        request={"content/json": PasswordSigninRequestSerializer},
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.Api4xxSerializer,
        },
    )
    def post(self, request):
        serializer = PasswordSigninRequestSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data["user"]
                response = Response(status=status.HTTP_204_NO_CONTENT)
                return set_new_auth_cookies(user, response)
        except serializers.ValidationError as e:
            if "error" in e.detail:
                raise BadRequest400(
                    code=e.detail["error"][0].code, detail=e.detail["error"][0]
                ) from e
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
