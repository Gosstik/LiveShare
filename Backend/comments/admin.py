from django.contrib import admin

from comments.models import Comment
from comments.models import CommentLike


admin.site.register([Comment, CommentLike])
