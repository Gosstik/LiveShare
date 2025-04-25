from rest_framework import serializers

import Backend.utils as utils

from users.models import User
from users.utils import UsersSearchUserType
from users.utils import USERS_SEARCH_USER_TYPES


class UserResponseSerializer(serializers.ModelSerializer, utils.StrictFieldsMixin):
    id = serializers.IntegerField()
    displayed_name = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'displayed_name',
        ]


class UsersV1SearchParamsSerializer(utils.StrictFieldsMixin):
    current_user_id = serializers.IntegerField(required=False)
    users_type = serializers.ChoiceField(
        required=False,
        choices=USERS_SEARCH_USER_TYPES,
        default=UsersSearchUserType.ALL,
    )


class UserV1SearchResponseSerializer(utils.StrictFieldsMixin):
    users = serializers.ListField(child=UserResponseSerializer())


class UsersV1FriendsInviteParamsSerializer(utils.StrictFieldsMixin):
    invited_user_id = serializers.IntegerField()


class UserV1FriendsRemoveParamsSerializer(utils.StrictFieldsMixin):
    removed_user_id = serializers.IntegerField()
