from django.urls import path

# from rest_framework import routers
# from posts.views import DeletePostViewSetV1
from posts.views import (
    CreatePostApiView,
    GetEditDeletePostApiView,
    GetPostsByFiltersApiView,
    PostLikeApiView,
    PostUnlikeApiView,
)

# router = routers.DefaultRouter(trailing_slash=False)
# router.register(r"v1/post", DeletePostViewSetV1)

urlpatterns = [
    # path("", include(router.urls)),
    path("v1/post/create", CreatePostApiView.as_view(), name="tmp-create-test"),
    path(
        "v1/post/<int:post_id>",
        GetEditDeletePostApiView.as_view(),
        name="get-edit-delete-post",
    ),
    path("v1/post/<int:post_id>/like", PostLikeApiView.as_view(), name="post-like"),
    path(
        "v1/post/<int:post_id>/unlike", PostUnlikeApiView.as_view(), name="post-unlike"
    ),
    path("v1/by-filters", GetPostsByFiltersApiView.as_view(), name="posts-by-filters"),
]
