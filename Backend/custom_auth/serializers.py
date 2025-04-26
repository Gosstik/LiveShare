from rest_framework import serializers

from users.serializers import UserResponseSerializer


class AuthTokenExpirationSerializer(serializers.Serializer):
    seconds_left = serializers.IntegerField()
    left_datetime = serializers.CharField()
    expiration_timestamp = serializers.CharField()


class AuthUserInfoResponseSerializer(serializers.Serializer):
    access_token_expiration = AuthTokenExpirationSerializer()
    user = UserResponseSerializer()
