from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import serializers

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes

import Backend.utils as utils

from users.models import User
from users.models import Friends
from users.utils import UsersSearchUserType
from users.serializers import UsersV1SearchParamsSerializer
from users.serializers import UserV1SearchResponseSerializer
from users.serializers import UsersV1FriendsInviteParamsSerializer
from users.serializers import UserV1FriendsRemoveParamsSerializer



# from api.mixins import ApiErrorsMixin, ApiAuthMixin, PublicApiMixin

# from auth.services import jwt_login, google_validate_id_token

# from users.services import user_get_or_create
# from users.selectors import user_get_me


# class UserMeApi(ApiAuthMixin, ApiErrorsMixin, APIView):
#     def get(self, request, *args, **kwargs):
#         return Response(user_get_me(user=request.user))


# class UserInitApi(PublicApiMixin, ApiErrorsMixin, APIView):
#     class InputSerializer(serializers.Serializer):
#         email = serializers.EmailField()
#         first_name = serializers.CharField(required=False, default='')
#         last_name = serializers.CharField(required=False, default='')

#     def post(self, request, *args, **kwargs):
#         id_token = request.headers.get('Authorization')
#         google_validate_id_token(id_token=id_token)

#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # We use get-or-create logic here for the sake of the example.
#         # We don't have a sign-up flow.
#         user, _ = user_get_or_create(**serializer.validated_data)

#         response = Response(data=user_get_me(user=user))
#         response = jwt_login(response=response, user=user)

#         return response


class UsersV1Search(APIView):
    @extend_schema(
        parameters=[
            UsersV1SearchParamsSerializer,
        ],
        responses={
            status.HTTP_200_OK: UserV1SearchResponseSerializer,
            status.HTTP_400_BAD_REQUEST: utils.BadRequestSerializer,
        },
    )
    def get(self, request: Request):
        params = utils.deserialize_or_400(
            UsersV1SearchParamsSerializer,
            request.query_params,
            detail="Request params deserialization failed",
        )
        if params['users_type'] == UsersSearchUserType.FRIENDS:
            # TODO: get info about current user with jwt ???
            utils.true_or_400(
                'current_user_id' in params,
                code='no_current_user_id',
                detail='current_user_id was not provided, but is required because of other filters'
            )
            friend_ids = Friends.objects.filter(user_id=params['current_user_id']).values_list('friend_id', flat=True)
            result_users = User.objects.filter(id__in=friend_ids)
        else:
            result_users = User.objects.all()

        response_data = {
            'users': result_users.order_by('first_name', 'last_name')
        }

        return utils.validate_and_get_response(
            response_data,
            UserV1SearchResponseSerializer,
            verbose_code="Serialization of response failed"
        )


class UserV1FriendsInviteApiView(APIView):
    @extend_schema(
        parameters=[
            UsersV1FriendsInviteParamsSerializer
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.BadRequestSerializer,
        },
    )
    def post(self, request):
        # TODO
        serializer = UserV1SearchResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return utils.get_serializer_errors_response(serializer)


class UserV1FriendsRemoveApiView(APIView):
    @extend_schema(
        parameters=[
            UserV1FriendsRemoveParamsSerializer
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.BadRequestSerializer,
        },
    )
    def post(self, request):
        # TODO
        serializer = UserV1FriendsRemoveParamsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return utils.get_serializer_errors_response(serializer)
