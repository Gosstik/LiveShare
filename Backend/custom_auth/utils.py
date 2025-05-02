import datetime as dt

from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

import Backend.utils as utils
from custom_auth.serializers import AuthUserInfoResponseSerializer
from users.serializers import UserResponseSerializer


def _get_token_expiration_data(
    request: Request,
    token_env_name,
    token_class,
):
    raw_token = request.COOKIES.get(settings.SIMPLE_JWT[token_env_name])
    token = token_class(raw_token)
    exp_datetime = token["exp"]

    exp_timestamp = dt.datetime.fromtimestamp(exp_datetime)
    left_datetime = exp_timestamp - dt.datetime.now()
    seconds_left = int(left_datetime.total_seconds())

    return {
        "seconds_left": seconds_left,
        "left_datetime": str(left_datetime),
        "expiration_timestamp": exp_timestamp.isoformat(),
    }


def get_auth_user_info(request: Request):
    access_token_expiration = _get_token_expiration_data(
        request, "AUTH_ACCESS_TOKEN", AccessToken
    )
    refresh_token_expiration = _get_token_expiration_data(
        request, "AUTH_REFRESH_TOKEN", RefreshToken
    )
    user_data = UserResponseSerializer(request.user).data
    response_data = {
        "access_token_expiration": access_token_expiration,
        "refresh_token_expiration": refresh_token_expiration,
        "user": user_data,
    }
    return utils.validate_and_get_response(
        response_data,
        AuthUserInfoResponseSerializer,
    )
