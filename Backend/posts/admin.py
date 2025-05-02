from django.contrib import admin

from posts.models import Post, PostLike

admin.site.register([Post, PostLike])
# admin.site.register([Posts])
