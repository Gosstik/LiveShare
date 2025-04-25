from django.contrib import admin

from posts.models import Post
from posts.models import PostLike


admin.site.register([Post, PostLike])
# admin.site.register([Posts])
