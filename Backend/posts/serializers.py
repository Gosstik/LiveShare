from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

import Backend.utils as utils
from users.serializers import UserResponseSerializer

from posts.models import Post


class PostSortFieldName(utils.EnumWithContains):
    CREATED_AT = "created_at"
    LIKES_COUNT = "likes_count"
    COMMENTS_COUNT = "comments_count"


POST_SORT_FIELD_NAMES = [(val.value, val.name) for val in PostSortFieldName]


def edit_post_request_example():
    return {"title": "Test post title", "text_content": "Text content"}


@extend_schema_serializer(
    examples=utils.single_example(edit_post_request_example()),
)
class EditPostRequestSerializer(serializers.ModelSerializer, utils.StrictFieldsMixin):
    # # TODO: add image and make it required=False (just delete)
    text_content = serializers.CharField(
        required=True,
    )

    class Meta:
        model = Post
        fields = ["title", "text_content"]


def create_post_request_example():
    return {
        "author_id": 1,
        **edit_post_request_example(),
    }


@extend_schema_serializer(
    examples=utils.single_example(create_post_request_example()),
)
class CreatePostRequestSerializer(EditPostRequestSerializer):
    author_id = serializers.IntegerField(
        required=True, help_text="Id of user that create post"
    )

    class Meta:
        model = Post
        fields = ["author_id", *EditPostRequestSerializer.Meta.fields]


class GetPostsByFiltersParamsSerializer(utils.StrictFieldsMixin):
    post_id = serializers.IntegerField(required=False)
    author_id = serializers.IntegerField(required=False)
    sort_field_name = serializers.ChoiceField(
        required=False,
        choices=POST_SORT_FIELD_NAMES,
        default=PostSortFieldName.CREATED_AT,
    )
    sort_type = serializers.ChoiceField(
        required=False,
        choices=utils.SORT_TYPES,
        default=utils.SortType.DESC,
    )
    post_title_search_str = serializers.CharField(
        required=False
    )



# TODO
def get_post_response_example():
    return {}


# @extend_schema_serializer(
#     examples=utils.single_example(get_post_response_example()),
# )
class GetPostResponseSerializer(serializers.ModelSerializer, utils.StrictFieldsMixin):
    id = serializers.IntegerField()
    author = UserResponseSerializer()
    likes_count = serializers.IntegerField()
    is_liked_by_user = serializers.BooleanField(
        required=True, help_text="Is post liked by current authenticated user"
    )
    comments_count = serializers.IntegerField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "text_content",
            "created_at",
            "edited_at",
            "likes_count",
            "is_liked_by_user",
            "comments_count",
        ]
        extra_kwargs = {
            "text_content": {"required": True},  # TODO: make it optional
        }


# TODO
def get_posts_by_filters_response_example():
    return {}


# @extend_schema_serializer(
#     examples=utils.single_example(get_post_response_example()),
# )
class GetPostsByFiltersResponseSerializer(utils.StrictFieldsMixin):
    posts = GetPostResponseSerializer(many=True)
