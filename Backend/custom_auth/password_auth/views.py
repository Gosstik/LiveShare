from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf

from custom_auth.utils import PublicApiMixin
from custom_auth.cookies import set_new_auth_cookies
from custom_auth.password_auth.serializers import (
    PasswordSignupRequestSerializer,
    PasswordSigninRequestSerializer
)

# TODO

class PasswordSignupApiView(PublicApiMixin, APIView):
    def post(self, request):
        serializer = PasswordSignupRequestSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                # TODO: add cookies
                print(f"!!! Created user: {user}")
                response = Response(status=status.HTTP_204_NO_CONTENT)
                return set_new_auth_cookies(user, response)
        except serializers.ValidationError as e:
            if 'email' in e.detail and "User with this email already exists" in str(e.detail['email'][0]):
                return Response(
                    {"error": "User with this email already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class PasswordSigninApiView(PublicApiMixin, APIView):
    def post(self, request):
        serializer = PasswordSigninRequestSerializer(data=request.data)
        
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                response = Response(status=status.HTTP_204_NO_CONTENT)
                return set_new_auth_cookies(user, response)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
