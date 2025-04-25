import json

from django.contrib.auth import login
from django.shortcuts import redirect

from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_auth.google_oauth.service import GoogleRawLoginFlowService
# from styleguide_example.users.selectors import user_list # TODO

from custom_auth.utils import PublicApiMixin
from custom_auth.utils import login_or_refresh_by_cookies
from users.models import User


class GoogleOAuthUrl(APIView, PublicApiMixin):
    def get(self, request, *args, **kwargs):
        google_login_flow = GoogleRawLoginFlowService()

        authorization_url, state = google_login_flow.get_authorization_url()

        # request.session["google_oauth2_state"] = state # TODO: remove

        # TODO: JUST RETURN body.url
        return Response(
            {"url" : authorization_url},
            status=status.HTTP_200_OK,
        )
        # return redirect(authorization_url)


class GoogleOAuthTokenLogin(APIView, PublicApiMixin):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        # state = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        # input_form = self.InputValidationForm(data=request.GET)

        # if not input_form.is_valid():
        #     return

        # validated_data = input_form.cleaned_data

        print("request.query_params=", request.query_params)
        code = request.query_params.get('code')
        # code = validated_data["code"] if validated_data.get("code") != "" else None
        # error = validated_data["error"] if validated_data.get("error") != "" else None
        error = request.query_params.get('error')
        # state = validated_data["state"] if validated_data.get("state") != "" else None

        if error is not None:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        # if code is None or state is None:
        #     return JsonResponse({"error": "Code and state are required"}, status=400)

        if code is None:
            print("HERE code!!!")
            return Response(
                {"error": "'code' is required but not presented"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # session_state = request.session.get("google_oauth2_state")

        # if session_state is None:
        #     return JsonResponse({"error": "CSRF check failed."}, status=400)

        # del request.session["google_oauth2_state"]

        # if state != session_state:
        #     return JsonResponse({"error": "CSRF check failed."}, status=400)

        google_login_flow = GoogleRawLoginFlowService()

        google_tokens = google_login_flow.get_tokens(code=code)
        id_token_decoded = google_tokens.decode_id_token()
        user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

        user_email = id_token_decoded["email"]
        # TODO: what if name changed? What if it is omitted?
        print("!!! user_info=", user_info)
        user, created = User.objects.get_or_create(
            email=user_email,
            first_name=user_info['given_name'],
            last_name=user_info['family_name'],
        )
        # user = user_queryset.first()
        # request_user_list = user_list(filters={"email": user_email}) # TODO
        # user = request_user_list.get() if request_user_list else None

        if user is None:
            message = f"Google OAuth: unable to find or create user with email={user_email}"
            return Response(
                {"error": message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # TODO: replace with jwt login

        # login(request, user) # TODO: remove

        result = {
            "id_token_decoded": id_token_decoded,
            "user_info": user_info, # TODO: probably remove ???
        }
        response = Response(result, status=status.HTTP_200_OK)
        response = login_or_refresh_by_cookies(user, response)

        # response.data = {
        #     **response.data,
        #     "id_token_decoded": id_token_decoded,
        #     "user_info": user_info, # TODO: probably remove ???
        # }
        # response.status_code = status.HTTP_200_OK
        # return response

        # TODO: start session ???

        return response
