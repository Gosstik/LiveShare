import datetime as dt
from django.db import models
from django.db.models.functions import Now

from users.models import User
from posts.models import Post

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(Post, db_column='post_id', on_delete=models.CASCADE)
    author = models.ForeignKey(User, db_column='author_id', on_delete=models.CASCADE)
    text_content = models.TextField()
    created_at = models.DateTimeField(db_default=Now())
    edited_at = models.DateTimeField(db_default=Now())

    class Meta:
        db_table = 'comments'
        indexes = [
            models.Index(fields=["created_at"], name="comments__created_at__idx"),
        ]
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        dots = "" if len(self.text_content) <= 12 else "..."
        return f"id={self.id}: {str(self.text_content)[0:12]}{dots}"

    def save(self, *args, **kwargs):
        if self.id:
            self.edited_at = dt.datetime.now()
        return super().save(*args, **kwargs)


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, db_column='comment_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment_likes'
        constraints = [
            models.UniqueConstraint(
                fields=['comment_id', 'user_id'], name='commentlike_pk'
            )
        ]
        verbose_name_plural = "Comment Likes"

    def __str__(self):
        return f'comment_id={self.comment.id}, user={self.user}'
