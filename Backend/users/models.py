from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.core.management.utils import get_random_secret_key


class User(AbstractUser):
    # username = None

    email = models.EmailField(unique=True, db_index=True)
    # TODO: add avatar
    # secret_key = models.CharField(max_length=255, default=get_random_secret_key)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name_plural = "Users"

    @property
    def name(self):
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

    def __str__(self):
        return str(self.email)

    # TODO: add phone and age


# from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
