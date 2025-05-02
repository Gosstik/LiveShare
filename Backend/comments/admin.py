from django.contrib import admin

from comments.models import Comment, CommentLike

admin.site.register([Comment, CommentLike])
