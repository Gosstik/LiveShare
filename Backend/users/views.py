from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from drf_spectacular.utils import extend_schema

import Backend.utils as utils
from Backend.exceptions import NotFound404
from custom_auth.mixins import PublicApiMixin

from users.models import User
from users.models import Friends
from users.models import FriendInvitation
from users.serializers import UsersV1SearchParamsSerializer
from users.serializers import UserV1SearchResponseSerializer
from users.utils import UsersSearchUserType
from users.utils import create_friends


class UsersV1Search(PublicApiMixin, APIView):
    @extend_schema(
        parameters=[
            UsersV1SearchParamsSerializer,
        ],
        responses={
            status.HTTP_200_OK: UserV1SearchResponseSerializer,
            status.HTTP_400_BAD_REQUEST: utils.Api4xxSerializer,
        },
    )
    def get(self, request: Request):
        params = utils.deserialize_or_400(
            UsersV1SearchParamsSerializer,
            request.query_params,
            detail="Request params deserialization failed",
        )
        if params['users_type'] == UsersSearchUserType.FRIENDS:
            utils.true_or_400(
                request.user.is_authenticated,
                code='invalid_filters',
                detail='Unauthorized request to list friends'
            )
            friend_ids = Friends.objects.filter(user=request.user).values_list('friend_id', flat=True)
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
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def post(self, request: Request, other_user_id: int):
        with transaction.atomic():
            cross_invitations = FriendInvitation.objects.filter(
                from_user_id=other_user_id,
                to_user=request.user,
            )
            if cross_invitations:
                create_friends(request.user.id, other_user_id)
                cross_invitations.delete()
            else:
                invitation, created = FriendInvitation.objects.get_or_create(
                    from_user=request.user,
                    to_user_id=other_user_id
                )
                if not created:
                    print(f"WARNING: invitation {invitation} already exists")

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserV1FriendsInviteCancelApiView(APIView):
    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: utils.Api4xxSerializer,
        },
    )
    def post(self, request: Request, other_user_id: int):
        with transaction.atomic():
            invitations = FriendInvitation.objects.filter(
                from_user=request.user,
                to_user_id=other_user_id,
            )
            if not invitations:
                raise NotFound404(detail="Invitation does not exist")
            invitations.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserV1FriendsInviteAcceptApiView(APIView):
    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: utils.Api4xxSerializer,
        },
    )
    def post(self, request: Request, other_user_id: int):
        with transaction.atomic():
            invitations = FriendInvitation.objects.filter(
                from_user_id=other_user_id,
                to_user=request.user
            )
            if not invitations:
                raise NotFound404(detail="Invitation does not exist")
            create_friends(request.user.id, other_user_id)
            invitations.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserV1FriendsInviteRejectApiView(APIView):
    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: utils.Api4xxSerializer,
        },
    )
    def post(self, request: Request, other_user_id: int):
        with transaction.atomic():
            invitations = FriendInvitation.objects.filter(
                from_user_id=other_user_id,
                to_user=request.user
            )
            if not invitations:
                raise NotFound404(detail="Invitation does not exist")
            invitations.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserV1FriendsRemoveApiView(APIView):
    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: utils.Api4xxSerializer,
        },
    )
    def post(self, request: Request, other_user_id: int):
        with transaction.atomic():
            friends = Friends.objects.filter(
                user=request.user,
                friend_id=other_user_id,
            )
            if not friends:
                raise NotFound404(detail="Users are not friends")
            friends.delete()
            Friends.objects.filter(
                user_id=other_user_id,
                friend=request.user,
            ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
