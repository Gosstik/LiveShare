from django.urls import path

from custom_auth.google_oauth.views import GoogleOAuthTokenLogin
from custom_auth.google_oauth.views import GoogleOAuthUrl

from custom_auth.views import LoginCheck
from custom_auth.views import SessionTokenRefresh
from custom_auth.views import Logout


google_oauth_urlpatterns = [
    path("oauth/google/url", GoogleOAuthUrl.as_view(), name="oauth-google-url"),
    path(
        "oauth/google/token/login",
        GoogleOAuthTokenLogin.as_view(),
        name="oauth-google-login",
    ),
]

urlpatterns = [
    *google_oauth_urlpatterns,
    path("login/default", GoogleOAuthUrl.as_view(), name="default-auth"),
    path("login/check", LoginCheck.as_view(), name="login-check"),
    path("token/refresh", SessionTokenRefresh.as_view(), name="token-refresh"),
    path("logout", Logout.as_view(), name="logout"),
]
