from django.urls import path, include

from custom_auth.views import AuthUserInfoApiView
from custom_auth.views import AuthTokenRefreshApiView
from custom_auth.views import AuthLogoutApiView


urlpatterns = [
    path("oauth/google/", include("custom_auth.google_oauth.urls")),
    path("password/", include("custom_auth.password_auth.urls")),
    path("user/info", AuthUserInfoApiView.as_view(), name="auth-user-info"),
    path("token/refresh", AuthTokenRefreshApiView.as_view(), name="auth-token-refresh"),
    path("logout", AuthLogoutApiView.as_view(), name="logout"),
]
