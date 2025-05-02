from django.urls import path

from comments.views import (
    CommentLikeApiView,
    CommentsForPostApiView,
    CommentUnlikeApiView,
    CreateCommentApiView,
    EditDeleteCommentApiView,
)

urlpatterns = [
    path("v1/comment/create", CreateCommentApiView.as_view(), name="create-comment"),
    path(
        "v1/comment/<int:comment_id>",
        EditDeleteCommentApiView.as_view(),
        name="edit-delete-comment",
    ),
    path(
        "v1/for-post/<int:post_id>",
        CommentsForPostApiView.as_view(),
        name="get-comments-by-filters",
    ),
    path(
        "v1/comment/<int:comment_id>/like",
        CommentLikeApiView.as_view(),
        name="comment-like",
    ),
    path(
        "v1/comment/<int:comment_id>/unlike",
        CommentUnlikeApiView.as_view(),
        name="comment-unlike",
    ),
]
