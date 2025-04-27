import datetime as dt
from typing import TYPE_CHECKING

from django.db.models.query import QuerySet
from django.db.models.functions import Now
from django.db import models

from users.models import User


if TYPE_CHECKING:
    from comments.models import Comment


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, db_column="author_id", on_delete=models.CASCADE)
    title = models.TextField()
    text_content = models.TextField(blank=True)
    attached_image = models.ImageField(
        upload_to="images/posts", blank=True, help_text="Attached image"
    )
    created_at = models.DateTimeField(db_default=Now()) # default=dt.datetime.now
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
            self.edited_at = dt.datetime.now()
        return super().save(*args, **kwargs)

    def get_related_comments(self) -> 'QuerySet[Comment]':
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


class Posts(models.Model):
    id = models.BigAutoField(primary_key=True)

class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
