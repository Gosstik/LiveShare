from django.urls import path, include

from custom_auth.views import AuthUserInfoApiView
from custom_auth.views import AuthTokenRefreshApiView
from custom_auth.views import AuthLogoutApiView


urlpatterns = [
    path("oauth/google/", include("custom_auth.google_oauth.urls")),
    # TODO: replace login check to get_user_info
    path("user/info", AuthUserInfoApiView.as_view(), name="login-check"),
    path("token/refresh", AuthTokenRefreshApiView.as_view(), name="token-refresh"),
    path("logout", AuthLogoutApiView.as_view(), name="logout"),
]
