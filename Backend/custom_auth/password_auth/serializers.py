from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class PasswordSigninRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                code="email_does_not_exist",
                detail={
                    "error": "User with that email does not exist"
                },
            )

        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError(
                code="invalid_password",
                detail={
                    "error": "Password is incorrect. Try again"
                },
            )

        data['user'] = user
        return data


class PasswordSignupRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    profile_icon = serializers.ImageField(required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def create(self, validated_data):
        # Generate a unique username from email
        username = validated_data['email'].split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        if 'profile_icon' in validated_data:
            user.profile_icon = validated_data['profile_icon']
            user.save()

        return user
