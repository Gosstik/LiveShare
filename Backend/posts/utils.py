from django.db.models import OuterRef
from django.db.models import Count
from django.db.models import Exists
from django.db.models import Subquery
from django.db.models import Value as V
from django.db.models.functions import Coalesce

import Backend.utils as utils
from Backend.exceptions import NotFound404
from users.models import User
from comments.models import Comment

from posts.models import Post
from posts.models import PostLike


class PostSortFieldName(utils.EnumWithContains):
    CREATED_AT = "created_at"
    LIKES_COUNT = "likes_count"
    COMMENTS_COUNT = "comments_count"


POST_SORT_FIELD_NAMES = [(val.value, val.name) for val in PostSortFieldName]


def get_post_or_404(post_id: int):
    return utils.get_object_or_404(
        lambda: Post.objects.get(id=post_id),
        error_detail=f"Post with post_id={post_id} not found",
    )


def post_404_response(post_id: int):
    return NotFound404(detail=f"Post with post_id={post_id} not found")


def get_posts_by_filters_from_db(params: dict, request_user: User):
    # Handle case for getting concrete post
    if "post_id" in params:
        result_set = Post.objects.filter(id=params["post_id"])
    else:
        result_set = Post.objects.all()

    if "post_title_search_str" in params:
        result_set = Post.objects.filter(title__icontains=params["post_title_search_str"])

    # Create subqueries for count fields
    comments_count_subquery = (
        Comment.objects.filter(post_id=OuterRef("pk"))
        .values("post_id")
        .annotate(count=Count("id"))
        .values("count")
    )
    likes_count_subquery = (
        PostLike.objects.filter(post_id=OuterRef("pk"))
        .values("post_id")
        .annotate(count=Count("id"))
        .values("count")
    )
    result_set = result_set.annotate(
        comments_count=Coalesce(Subquery(comments_count_subquery), V(0))
    ).annotate(likes_count=Coalesce(Subquery(likes_count_subquery), V(0)))

    # Sorting
    sort_field_name = params["sort_field_name"]
    if params["sort_type"] == utils.SortType.DESC:
        sort_field_name = f"-{params['sort_field_name']}"
    result_set = result_set.order_by(sort_field_name)

    # Filtering by user
    if "author_id" in params:
        result_set = result_set.filter(author__id=params["author_id"])

    # Set is_liked_by_user
    if request_user.is_authenticated:
        like_exists_subquery = PostLike.objects.filter(
            post_id=OuterRef("pk"), user_id=request_user.id
        )
        result_set = result_set.annotate(is_liked_by_user=Exists(like_exists_subquery))
    else:
        result_set = result_set.annotate(is_liked_by_user=V(False))

    return result_set.all()


def transform_db_posts_for_response(posts):
    # TODO: (profiling) prefetch author
    posts_data = []
    for post in posts:
        author_display_name = utils.get_user_display_name(
            post.author.email,
            post.author.first_name,
            post.author.last_name,
        )
        posts_data.append(
            {
                "post_id": post.id,
                "author_id": post.author.id,
                "author_email": post.author.email,
                "author_display_name": author_display_name,
                "title": post.title,
                "text_content": post.text_content,
                "created_at": post.created_at,
                "edited_at": post.edited_at,
                "likes_count": post.likes_count,
                "is_liked_by_user": post.is_liked_by_user,
                "comments_count": post.comments_count,
                # TODO: add user emails that liked
            }
        )
    return posts_data
