import os
from django.conf import settings
from django.shortcuts import redirect
from django.core.files.base import ContentFile
import requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse

import Backend.utils as utils
from Backend.exceptions import BadRequest400

from custom_auth.google_oauth.service import GoogleRawLoginFlowService
from custom_auth.google_oauth.serializers import GoogleOAuthCallbackParamsSerializer

from custom_auth.mixins import PublicApiMixin
from custom_auth.cookies import set_new_auth_cookies
from users.models import User


# Ensure media/profile_icons directory exists
media_root = settings.MEDIA_ROOT
profile_icons_dir = os.path.join(media_root, 'profile_icons')
os.makedirs(profile_icons_dir, exist_ok=True)


class GoogleOAuthRedirect(PublicApiMixin, APIView):
    @extend_schema(
        description="Initiates Google OAuth2 flow by redirecting to Google's authorization page",
        responses={
            status.HTTP_302_FOUND: OpenApiResponse(
                response=None,
                description="Redirect to Google's authorization page with account selection",
            ),
        },
    )
    def get(self, request):
        google_login_flow = GoogleRawLoginFlowService()
        authorization_url, state = google_login_flow.get_authorization_url()
        request.session["google_oauth2_state"] = state
        return redirect(authorization_url)


class GoogleOAuthCallbackApiView(PublicApiMixin, APIView):
    @extend_schema(
        description="Handles the OAuth2 callback from Google after user authorization",
        parameters=[
            GoogleOAuthCallbackParamsSerializer,
        ],
        responses={
            status.HTTP_302_FOUND: OpenApiResponse(
                response=None,
                description=(
                    "Redirect with authentication cookies.\n\n"
                    "**Headers:**\n"
                    f"- `Location`: {settings.AUTH_REDIRECT_FRONTEND_URL}\n"
                    f"- `Set-Cookie`: {settings.SIMPLE_JWT['AUTH_ACCESS_TOKEN']}=[value]; HttpOnly; Path=/\n"
                    f"- `Set-Cookie`: {settings.SIMPLE_JWT['AUTH_REFRESH_TOKEN']}=[value]; HttpOnly; Path=/"
                )
            ),
            status.HTTP_400_BAD_REQUEST: utils.Api4xxSerializer,
        },
    )
    def get(self, request: Request):
        params = utils.deserialize_or_400(
            request.query_params,
            GoogleOAuthCallbackParamsSerializer,
            detail="Request params deserialization failed",
        )

        self._check_error(params)
        self._check_greenflow_params(params)
        self._check_csrf_state(request, params['state'])

        # Logic with authorization
        google_login_flow = GoogleRawLoginFlowService()

        google_tokens = google_login_flow.get_tokens_by_code(code=params['code'])
        id_token_decoded = google_tokens.decode_id_token()
        # user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

        user, created = User.objects.get_or_create(
            email=id_token_decoded["email"],
            defaults={
                'first_name': id_token_decoded['given_name'],
                'last_name': id_token_decoded.get('family_name', ''),
            }
        )

        self._save_profile_icon(id_token_decoded, user)

        if user is None:
            raise BadRequest400(
                code='google_oauth_error',
                detail=f"google oauth error: unable to find or create user with email={id_token_decoded['email']}"
            )

        # TODO: what if name changed? What if it is omitted?
        # We need to update name

        response = redirect(settings.AUTH_REDIRECT_FRONTEND_URL)
        return set_new_auth_cookies(user, response)

    ############################################################################
    ### Internals

    def _check_error(self, params):
        if 'error' in params:
            # TODO: handle exception to show user
            raise BadRequest400(
                code='google_oauth_error',
                detail=f"google oauth error: {params['error']}"
            )

    def _check_greenflow_params(self, params):
        if 'code' not in params:
            # TODO: handle exception to show user
            raise BadRequest400(
                code='google_oauth_error',
                detail="google oauth error: 'code' is required but not presented"
            )

        if 'state' not in params:
            # TODO: handle exception to show user
            raise BadRequest400(
                code='google_oauth_error',
                detail="google oauth error: 'state' is required but not presented. You are potentially under CSRF attack!!!"
            )

    def _check_csrf_state(self, request: Request, params_state):
        session_state = request.session.get("google_oauth2_state")
        if session_state is None:
            # TODO: handle exception to show user
            raise BadRequest400(
                code='csrf_oauth_failed',
                detail='CSRF check for oauth failed: no session state detected'
            )
        del request.session["google_oauth2_state"]

        if params_state != session_state:
            # TODO: handle exception to show user
            raise BadRequest400(
                code='csrf_oauth_failed',
                detail='CSRF check for oauth failed: session state differs params state'
            )

    def _save_profile_icon(self, id_token_decoded, user: User):
        if 'picture' not in id_token_decoded:
            return
        try:
            # Download and save the image
            response = requests.get(id_token_decoded['picture'], stream=True)
            if response.status_code == 200:
                # Delete old file if exists
                if user.profile_icon:
                    old_file_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_icon))
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                    user.profile_icon = None
                    user.save()

                # Save new file
                image_content = ContentFile(response.content)
                filename = f"profile_{user.id}.jpg"
                user.profile_icon.save(filename, image_content, save=True)
                print(f"!!! Profile icon saved to: {user.profile_icon.path}")
        except Exception as e:
            print(f"Failed to save profile icon for user={user.id}: {str(e)}")
