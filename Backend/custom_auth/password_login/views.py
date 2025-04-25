from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf

from custom_auth.utils import login_or_refresh_by_cookies


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class PasswordLogin(APIView):
    def post(self, request):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"Invalid" : "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        response = login_or_refresh_by_cookies(user, response)
        return response
