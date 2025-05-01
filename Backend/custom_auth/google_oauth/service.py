from random import SystemRandom
from typing import Any, Dict
from urllib.parse import urlencode

import jwt
import requests
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET


@define
class GoogleRawLoginCredentials:
    client_id: str
    client_secret: str


@define
class GoogleAccessTokens:
    id_token: str
    access_token: str

    def decode_id_token(self) -> Dict[str, str]:
        id_token = self.id_token
        decoded_token = jwt.decode(jwt=id_token, options={"verify_signature": False})
        return decoded_token


class GoogleRawLoginFlowService:
    # That url is used on frontend to redirect to google oauth
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    # These urls are used on backend, so they need to be overrided from .env
    # in docker to make requests through nginx
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = settings.GOOGLE_ACCESS_TOKEN_OBTAIN_URL
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = ['openid', 'profile', 'email']

    def __init__(self):
        self._credentials = google_raw_login_get_credentials()

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        host = settings.BACKEND_BASE_URL
        path = settings.GOOGLE_OAUTH2_CALLBACK_PATH
        return f"{host}/{path}"

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()
        state = self._generate_state_session_token()
        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
            # "prompt": "consent",
        }

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state

    def get_tokens_by_code(self, *, code: str) -> GoogleAccessTokens:
        redirect_uri = self._get_redirect_uri()

        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
        data = {
            "code": code,
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        # TODO: handle exceeded timeout
        print(f"!!!!! Before token request, self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL={self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL}")
        response = requests.post(
            self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
            data=data,
            timeout=4, # 4 seconds
        )
        print("!!!!! After token request")

        if not response.ok:
            raise RuntimeError("Failed to obtain access token from Google.")

        # TODO: replace with serializer
        tokens = response.json()
        google_tokens = GoogleAccessTokens(
            id_token=tokens["id_token"],
            access_token=tokens["access_token"],
        )

        return google_tokens

    # TODO: remove it ? It is not used, only needed for offline access
    def get_user_info(self, *, google_tokens: GoogleAccessTokens) -> Dict[str, Any]:
        access_token = google_tokens.access_token
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
        response = requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={"access_token": access_token},
            timeout=4,
        )

        if not response.ok:
            raise RuntimeError("Failed to obtain user info from Google")

        return response.json()


def google_raw_login_get_credentials() -> GoogleRawLoginCredentials:
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET

    if not client_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_ID missing in env")

    if not client_secret:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_SECRET missing in env")

    credentials = GoogleRawLoginCredentials(
        client_id=client_id,
        client_secret=client_secret,
    )

    return credentials
