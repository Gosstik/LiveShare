from django.db.models import OuterRef
from django.db.models import Count
from django.db.models import Exists
from django.db.models import Subquery
from django.db.models import Value as V
from django.db.models.functions import Coalesce

import Backend.utils as utils
from users.models import User
from posts.utils import get_post_or_404

from comments.models import Comment
from comments.models import CommentLike


class CommentsSortFieldName(utils.EnumWithContains):
    CREATED_AT = "created_at"
    LIKES_COUNT = "likes_count"


COMMENT_SORT_FIELD_NAMES = [(val.value, val.name) for val in CommentsSortFieldName]


def get_comment_or_404(comment_id: int):
    return utils.get_object_or_404(
        lambda: Comment.objects.get(id=comment_id),
        error_detail=f"Comment with comment_id={comment_id} not found",
    )


def make_comments_by_filters_query(params: dict, request_user: User):
    post = get_post_or_404(params["post_id"])
    result_set = post.comment_set.all()

    # Create subqueries for count fields
    likes_count_subquery = (
        CommentLike.objects.filter(comment_id=OuterRef("pk"))
        .values("user_id")
        .annotate(count=Count("id"))
        .values("count")
    )
    result_set = result_set.annotate(
        likes_count=Coalesce(Subquery(likes_count_subquery), V(0))
    )

    # Sorting
    sort_field_name = params["sort_field_name"]
    if params["sort_type"] == utils.SortType.DESC:
        sort_field_name = f"-{params['sort_field_name']}"
    result_set = result_set.order_by(sort_field_name)

    # Set is_liked_by_user
    if request_user.is_authenticated:
        like_exists_subquery = CommentLike.objects.filter(
            comment_id=OuterRef("pk"), user_id=request_user.id
        )
        result_set = result_set.annotate(is_liked_by_user=Exists(like_exists_subquery))
    else:
        result_set = result_set.annotate(is_liked_by_user=V(False))

    return result_set
