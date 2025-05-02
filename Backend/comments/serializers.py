from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

import Backend.utils as utils
from comments.models import Comment
from comments.utils import COMMENT_SORT_FIELD_NAMES, CommentsSortFieldName
from users.serializers import UserResponseSerializer

################################################################################

### Helpers


def transform_db_comments_for_response(filtered_comments):
    # TODO: (profiling) prefetch author
    comments_data = []
    for comment in filtered_comments:
        comments_data.append(CommentForPostSerializer(comment).data)

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

    class Meta:
        model = Comment
        fields = ["post_id", "author_id", *EditCommentRequestSerializer.Meta.fields]

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request_user")
        return Comment.objects.create(**validated_data)


def comment_by_post_example():
    return {
        "author_id": 1,
        **edit_comment_request_example(),
    }


class CommentsByFiltersParamsSerializer(utils.StrictFieldsMixin):
    sort_field_name = serializers.ChoiceField(
        required=False,
        choices=COMMENT_SORT_FIELD_NAMES,
        default=CommentsSortFieldName.CREATED_AT,
    )
    sort_type = serializers.ChoiceField(
        required=False,
        choices=utils.SORT_TYPES,
        default=utils.SortType.DESC,
    )


@extend_schema_serializer(
    examples=utils.single_example(comment_by_post_example()),
)
class CommentForPostSerializer(serializers.ModelSerializer, utils.StrictFieldsMixin):
    id = serializers.IntegerField()
    author = UserResponseSerializer()
    likes_count = serializers.IntegerField()
    is_liked_by_user = serializers.BooleanField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "text_content",
            "created_at",
            "edited_at",
            "likes_count",
            "is_liked_by_user",
        ]


# TODO: schema example
class CommentsForPostSerializer(utils.StrictFieldsMixin):
    post_id = serializers.IntegerField()
    comments = CommentForPostSerializer(many=True)
