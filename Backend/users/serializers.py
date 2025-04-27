from rest_framework import serializers

import Backend.utils as utils

from users.models import User
from users.utils import UsersSearchUserType
from users.utils import USERS_SEARCH_USER_TYPES
from users.utils import UserFriendStatus
from users.utils import USER_FRIEND_STATUSES


class UserResponseSerializer(serializers.ModelSerializer, utils.StrictFieldsMixin):
    id = serializers.IntegerField()
    email = serializers.CharField()
    displayed_name = serializers.CharField()
    profile_icon_url = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'displayed_name',
            'profile_icon_url',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove all None values from the output
        # for field in ['profile_icon_url', 'other_optional_field']:  # Add fields as needed
        for field in self.fields.keys():  # Add fields as needed
            if representation.get(field) is None:
                representation.pop(field, None)
        return representation


class UsersV1SearchParamsSerializer(utils.StrictFieldsMixin):
    users_type = serializers.ChoiceField(
        required=False,
        choices=USERS_SEARCH_USER_TYPES,
        default=UsersSearchUserType.ALL,
    )


class UserSearchResponseSerializer(UserResponseSerializer):
    friend_status = serializers.ChoiceField(
        required=False,
        choices=USER_FRIEND_STATUSES,
    )

    class Meta(UserResponseSerializer.Meta):
        fields = UserResponseSerializer.Meta.fields + ['friend_status']


class UsersSearchResponseSerializer(serializers.Serializer):
    users = serializers.ListField(child=UserSearchResponseSerializer())
