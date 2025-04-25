from django.db import models
from django.db.models.functions import Now
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
    def displayed_name(self):
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

    def __str__(self):
        return str(self.email)

    # TODO: add phone and age


# class Post(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     author = models.ForeignKey(User, db_column="author_id", on_delete=models.CASCADE)
#     title = models.TextField()
#     text_content = models.TextField(blank=True)
#     attached_image = models.ImageField(
#         upload_to="images/posts", blank=True, help_text="Attached image"
#     )
#     created_at = models.DateTimeField(db_default=Now()) # default=dt.datetime.now
#     edited_at = models.DateTimeField(db_default=Now())

#     class Meta:
#         db_table = "posts"
#         indexes = [
#             models.Index(fields=["created_at"], name="posts__created_at__idx"),
#         ]
#         verbose_name_plural = "Posts"
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"{str(self.id)}, {str(self.author)}: {str(self.title)}"

#     def save(self, *args, **kwargs):
#         if self.id:
#             self.edited_at = dt.datetime.now()
#         return super().save(*args, **kwargs)


class Friends(models.Model):
    user = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, db_column="friend_id", on_delete=models.CASCADE, related_name="friend")

    class Meta:
        db_table = "friends"
        verbose_name_plural = "Friends"
        constraints = [
            models.UniqueConstraint(fields=["user_id", "friend_id"], name="friends_pk")
        ]

    def __str__(self):
        return f'{str(self.id)}: ({str(self.user_id)}, {str(self.friend_id)})'


class FriendInvitation(models.Model):
    from_user = models.ForeignKey(User, db_column="from_user_id", on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, db_column="to_user_id", on_delete=models.CASCADE, related_name="to_user")
    created_at = models.DateTimeField(db_default=Now())

    class Meta:
        db_table = "friend_invitations"
        verbose_name_plural = "Friend Invitations"
        constraints = [
            models.UniqueConstraint(fields=["from_user_id", "to_user_id"], name="friendinvitations_pk")
        ]

    def __str__(self):
        return f'{str(self.user_id)} -> {str(self.friend_id)}'


# from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
