from rest_framework import serializers

import Backend.utils as utils


class GoogleOAuthCallbackParamsSerializer(serializers.Serializer):
    state = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    code = serializers.CharField(required=False)
