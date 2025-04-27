from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf

from drf_spectacular.utils import extend_schema

import Backend.utils as utils
from Backend.exceptions import BadRequest400

from custom_auth.mixins import PublicApiMixin
from custom_auth.cookies import set_new_auth_cookies
from custom_auth.password_auth.serializers import (
    PasswordSignupRequestSerializer,
    PasswordSigninRequestSerializer
)


class PasswordSignupApiView(PublicApiMixin, APIView):
    @extend_schema(
        request={
            'multipart/form-data': PasswordSignupRequestSerializer,
        },
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.Api4xxSerializer,
        }
    )
    def post(self, request):
        serializer = PasswordSignupRequestSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                response = Response(status=status.HTTP_204_NO_CONTENT)
                return set_new_auth_cookies(user, response)
        except serializers.ValidationError as e:
            if 'email' in e.detail and "User with this email already exists" in str(e.detail['email'][0]):
                raise BadRequest400(
                    code="email_already_exists",
                    detail="User with this email already exists",
                )
            raise BadRequest400(detail=e.detail)


class PasswordSigninApiView(PublicApiMixin, APIView):
    @extend_schema(
        request={
            'content/json': PasswordSigninRequestSerializer
        },
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.Api4xxSerializer,
        }
    )
    def post(self, request):
        serializer = PasswordSigninRequestSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                response = Response(status=status.HTTP_204_NO_CONTENT)
                return set_new_auth_cookies(user, response)
        except serializers.ValidationError as e:
            if 'error' in e.detail:
                raise BadRequest400(code=e.detail['error'][0].code, detail=e.detail['error'][0])
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
