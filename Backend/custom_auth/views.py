from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes

from custom_auth.utils import (
    ApiErrorsMixin,
    PublicApiMixin,
    AuthApiMixin,
    login_or_refresh_by_cookies,
)


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


#       try {
#     // Get token from cookie
#     const token = req.cookies.token;

#     console.log(`logged_in req=`, req);
#     if (!token) {
#       console.log(`logged_in !token => false`);
#       res.json({ loggedIn: false });
#       return;
#     }
#     // var now = new Date();
#     // var time = now.getTime();
#     // var expireTime = time + config.tokenExpiration;
#     // var expireTime = time;
#     // now.setTime(expireTime);

#     const { user } = jwt.verify(token, config.tokenSecret);
#     console.log(`logged_in user=`, user);
#     const newToken = jwt.sign({ user }, config.tokenSecret, {
#       // expiresIn: config.tokenExpiration,
#       expiresIn: config.tokenExpiration,
#     });

#     // Reset token in cookie
#     res.cookie("token", newToken, {
#       maxAge: config.tokenExpiration,
#       httpOnly: true,
#     });
#     res.json({ loggedIn: true, user });
#     console.log(`logged_in res=${res}`);
#   } catch (err) {
#     console.log(`logged_in CATCH res=${res}`);
#     res.json({ loggedIn: false });
#   }


class SessionTokenRefresh(APIView, AuthApiMixin, ApiErrorsMixin):
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_REFRESH_TOKEN"])
        # TODO: replace JWTAuthentication with CookieJWTAuthentication ???
        jwt_object = JWTAuthentication()
        # TODO: skip ??? To manage 401
        # TODO: in case invalid token must logout user
        validated_token = jwt_object.get_validated_token(refresh_token)
        print(f"!!! refresh_validated_token={validated_token}")
        user = jwt_object.get_user(validated_token)

        response = Response(status=status.HTTP_200_OK)
        response = login_or_refresh_by_cookies(user, response)
        return response
        # TODO
        # response = Response(status=status.HTTP_200_OK)
        # response.set_cookie(
        #     settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN'],


class Logout(APIView, AuthApiMixin, ApiErrorsMixin):
    def post(self, request):
        # user_change_secret_key(user=request.user)

        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_ACCESS_TOKEN"])
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_REFRESH_TOKEN"])

        return response
