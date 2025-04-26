from django.urls import path, include

from custom_auth.google_oauth.views import GoogleOAuthCallbackApiView
from custom_auth.google_oauth.views import GoogleOAuthRedirect

from custom_auth.views import LoginCheck
from custom_auth.views import SessionTokenRefresh
from custom_auth.views import Logout


# google_oauth_urlpatterns = [
#     path("oauth/google/url", GoogleOAuthRedirect.as_view(), name="oauth-google-url"),
#     path(
#         "oauth/google/token/login",
#         GoogleOAuthCallback.as_view(),
#         name="oauth-google-login",
#     ),
# ]

urlpatterns = [
    path("oauth/google/", include("custom_auth.google_oauth.urls")),
    # *google_oauth_urlpatterns,
    path("login/default", GoogleOAuthRedirect.as_view(), name="default-auth"),
    path("login/check", LoginCheck.as_view(), name="login-check"),
    path("token/refresh", SessionTokenRefresh.as_view(), name="token-refresh"),
    path("logout", Logout.as_view(), name="logout"),
]
