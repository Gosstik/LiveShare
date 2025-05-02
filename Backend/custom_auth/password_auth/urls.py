from django.urls import path

from custom_auth.password_auth.views import PasswordSigninApiView, PasswordSignupApiView

urlpatterns = [
    path("signup", PasswordSignupApiView.as_view(), name="auth-password-signup"),
    path(
        "signin",
        PasswordSigninApiView.as_view(),
        name="auth-password-signin",
    ),
]
