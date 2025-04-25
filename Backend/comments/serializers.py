from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

import Backend.utils as utils

from comments.models import Comment
from comments.utils import COMMENT_SORT_FIELD_NAMES
from comments.utils import CommentsSortFieldName

################################################################################

### Helpers

def transform_db_comments_for_response(filtered_comments):
    # TODO: (profiling) prefetch author
    comments_data = []
    for comment in filtered_comments:
        author_display_name = utils.get_user_display_name(
            comment.author.email,
            comment.author.first_name,
            comment.author.last_name,
        )

        # TODO: add user profile image
        comment_data = {
            "comment_id": comment.id,
            "author_id": comment.author.id,
            "author_email": comment.author.email,
            "author_display_name": author_display_name,
            "text_content": comment.text_content,
            "created_at": comment.created_at,
            "edited_at": comment.edited_at,
            "likes_count": comment.likes_count,
            "is_liked_by_user": comment.is_liked_by_user,
        }
        utils.validate_data(
            comment_data,
            CommentByFiltersSerializer,
            verbose_code=f"Validation for comment_id={comment.id}",
        )
        comments_data.append(comment_data)

    return comments_data

################################################################################

### Serializers


def edit_comment_request_example():
    return {"text_content": "Comment text content"}


@extend_schema_serializer(
    examples=utils.single_example(edit_comment_request_example()),
)
class EditCommentRequestSerializer(
    serializers.ModelSerializer, utils.StrictFieldsMixin
):
    class Meta:
        model = Comment
        fields = ["text_content"]


def create_comment_request_example():
    return {
        "post_id": 1,
        "author_id": 1,
        **edit_comment_request_example(),
    }


@extend_schema_serializer(
    examples=utils.single_example(create_comment_request_example()),
)
class CreateCommentRequestSerializer(EditCommentRequestSerializer):
    post_id = serializers.IntegerField()
    author_id = serializers.IntegerField(help_text="Id of user that create comment")

    class Meta:
        model = Comment
        fields = ["post_id", "author_id", *EditCommentRequestSerializer.Meta.fields]


def comment_by_post_example():
    return {
        "author_id": 1,
        **edit_comment_request_example(),
    }


class CommentsByFiltersParamsSerializer(utils.StrictFieldsMixin):
    post_id = serializers.IntegerField(required=True)
    sort_field_name = serializers.ChoiceField(
        required=False,
        choices=COMMENT_SORT_FIELD_NAMES,
        default=CommentsSortFieldName.CREATED_AT.value,
    )
    sort_type = serializers.ChoiceField(
        required=False,
        choices=utils.SORT_TYPES,
        default=utils.SortType.DESC.value,
    )


@extend_schema_serializer(
    examples=utils.single_example(comment_by_post_example()),
)
class CommentByFiltersSerializer(
    serializers.ModelSerializer, utils.StrictFieldsMixin
):
    comment_id = serializers.IntegerField()
    author_id = serializers.IntegerField(help_text="Id of user that create comment")
    author_email = serializers.CharField()
    author_display_name = serializers.CharField()
    likes_count = serializers.IntegerField()
    is_liked_by_user = serializers.BooleanField()

    class Meta:
        model = Comment
        fields = [
            "comment_id",
            "author_id",
            "author_email",
            "author_display_name",
            "text_content",
            "created_at",
            "edited_at",
            "likes_count",
            "is_liked_by_user",
        ]


# TODO: schema example
class CommentsByFilterSerializer(utils.StrictFieldsMixin):
    post_id = serializers.IntegerField()
    comments = CommentByFiltersSerializer(many=True)
