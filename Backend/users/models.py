from django.conf import settings
from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # username = None

    email = models.EmailField(unique=True, db_index=True)
    profile_icon = models.ImageField(
        upload_to='profile_icons',
        null=True,
        blank=True,
        verbose_name='Profile Icon',
        help_text='User profile picture'
    )

    @property
    def profile_icon_url(self):
        if self.profile_icon:
            try:
                return f"{settings.BACKEND_BASE_URL}{self.profile_icon.url}"
            except Exception as e:
                print(f"Error getting profile_icon_url: {str(e)}")
        return None

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
        return f'{self.from_user.id} -> {self.to_user.id} ({str(self.from_user)} -> {str(self.to_user)})'
