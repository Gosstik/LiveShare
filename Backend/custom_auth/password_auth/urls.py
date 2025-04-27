from django.urls import path

from custom_auth.password_auth.views import PasswordSignupApiView
from custom_auth.password_auth.views import PasswordSigninApiView


urlpatterns = [
    path("signup", PasswordSignupApiView.as_view(), name="auth-password-signup"),
    path(
        "signin",
        PasswordSigninApiView.as_view(),
        name="auth-password-signin",
    ),
]
