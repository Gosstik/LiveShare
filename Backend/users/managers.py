# from django.contrib.auth.base_user import BaseUserManager

# class CustomUserManager(BaseUserManager):
#     def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
#         if not email:
#             raise ValueError('Steam name must be set')
#         user = self.model(
#             email=email,
#             is_active=True,
#             is_staff=is_staff,
#             is_superuser=is_superuser,
#             **extra_fields,
#         )
#         if password:
#             user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, password=None, **extra_fields):
#         return self._create_user(
#             extra_fields['name'],
#             password,
#             False,
#             False,
#             **extra_fields,
#         )

#     def create_superuser(self, email, password=None, **extra_fields):
#         return self._create_user(email, password, True, True, **extra_fields)
