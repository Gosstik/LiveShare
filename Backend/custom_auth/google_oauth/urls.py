from django.urls import path

from custom_auth.google_oauth.views import GoogleOAuthCallbackApiView
from custom_auth.google_oauth.views import GoogleOAuthRedirect


urlpatterns = [
    path("redirect", GoogleOAuthRedirect.as_view(), name="oauth-google-redirect"),
    path(
        "callback",
        GoogleOAuthCallbackApiView.as_view(),
        name="oauth-google-callback",
    ),
]
