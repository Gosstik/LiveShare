from rest_framework import serializers


class GoogleOAuthCallbackParamsSerializer(serializers.Serializer):
    state = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    code = serializers.CharField(required=False)
