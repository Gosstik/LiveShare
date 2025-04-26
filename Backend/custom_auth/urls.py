from django.urls import path, include

from custom_auth.google_oauth.views import GoogleOAuthRedirect

from custom_auth.views import LoginCheck
from custom_auth.views import AuthTokenRefreshApiView
from custom_auth.views import LogoutApiView


urlpatterns = [
    path("oauth/google/", include("custom_auth.google_oauth.urls")),
    # TODO: replace login check to get_user_info
    path("login/check", LoginCheck.as_view(), name="login-check"),
    path("token/refresh", AuthTokenRefreshApiView.as_view(), name="token-refresh"),
    path("logout", LogoutApiView.as_view(), name="logout"),
]
