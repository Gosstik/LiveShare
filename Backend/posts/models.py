from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models.functions import Now
from django.db.models.query import QuerySet
from django.utils import timezone

from users.models import User

if TYPE_CHECKING:
    from comments.models import Comment


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, db_column="author_id", on_delete=models.CASCADE)
    title = models.TextField()
    text_content = models.TextField()
    attached_image = models.ImageField(
        upload_to="posts_attached_images",
        null=True,
        blank=True,
        verbose_name="Post Image",
        help_text="Attached image",
    )

    @property
    def attached_image_url(self):
        if self.attached_image:
            try:
                return f"{settings.BACKEND_BASE_URL}{self.attached_image.url}"
            except Exception as e:
                print(f"Error getting attached_image_url: {str(e)}")
        return None

    @property
    def likes_count(self) -> int:
        return self.postlike_set.count()

    @likes_count.setter
    def likes_count(self, value):
        # Required for Django's annotation system
        self._likes_count = value

    @property
    def comments_count(self) -> int:
        return self.comment_set.count()

    @comments_count.setter
    def comments_count(self, value):
        # Required for Django's annotation system
        self._comments_count = value

    created_at = models.DateTimeField(db_default=Now())
    edited_at = models.DateTimeField(db_default=Now())

    class Meta:
        db_table = "posts"
        indexes = [
            models.Index(fields=["created_at"], name="posts__created_at__idx"),
        ]
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{str(self.id)}, {str(self.author)}: {str(self.title)}"

    def save(self, *args, **kwargs):
        if self.id:
            self.edited_at = timezone.now()
        return super().save(*args, **kwargs)

    def get_related_comments(self) -> "QuerySet[Comment]":
        return self.comment_set.all()


class PostLike(models.Model):
    # pk = models.CompositePrimaryKey("post_id", "user_id")
    post = models.ForeignKey(Post, db_column="post_id", on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE)

    class Meta:
        db_table = "post_likes"
        constraints = [
            models.UniqueConstraint(fields=["post_id", "user_id"], name="postlikes_pk")
        ]
        verbose_name_plural = "Post Likes"

    def __str__(self):
        return f"post_id={self.post.id}, user={self.user}"


class PostView(models.Model):
    post = models.ForeignKey(Post, db_column="post_id", on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE)

    class Meta:
        db_table = "post_views"
        constraints = [
            models.UniqueConstraint(fields=["post_id", "user_id"], name="postviews_pk")
        ]
        verbose_name_plural = "Post Views"

    def __str__(self):
        return f"post_id={self.post.id}, user={self.user}"
