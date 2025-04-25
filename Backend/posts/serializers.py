from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

import Backend.utils as utils

from posts.models import Post
from posts.utils import PostSortFieldName
from posts.utils import POST_SORT_FIELD_NAMES


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


# @extend_schema_serializer(
#     examples=utils.single_example(create_post_request_example()),
# )
# class CreatePostRequestSerializer(serializers.ModelSerializer, utils.StrictFieldsMixin):
#     author_id = serializers.IntegerField(
#         required=True, help_text="Id of user that create post"
#     )
#     # # TODO: add image and make it required=False (just delete)
#     text_content = serializers.CharField(
#         required=True,
#     )

#     class Meta:
#         model = Post
#         fields = ["author_id", "title", "text_content"]
###########################################################

# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     utils.set_default_help_text_from_model(self)

# run_validation
# def run_validation(self, data=None):
#     raise serializers.ValidationError()

# {'title': [ErrorDetail(string='This field is required.', code='required')]}
# {'title': [ErrorDetail(string='This field is required.', code='required')]}

# def to_internal_value(self, data):
#     raise serializers.ValidationError({"field": "some error"})

# def to_internal_value(self, data):
#     # raise RuntimeError("Custom error")
#     # raise serializers.ValidationError(code="some_code", detail="more_detail")
#     raise RuntimeError("some error")
#     raise serializers.ValidationError({
#         "Some error"
#     })
#     print("HEEEREEEE")
#     if not isinstance(data, dict):
#         raise serializers.ValidationError("Expected a dictionary of items")

#     unknown_fields = set(data.keys()) - set(self.fields.keys())
#     if unknown_fields:
#         raise serializers.ValidationError({
#             f"Additional properties are not allowed, but got [{unknown_fields}]"
#         }
#         )

#     return super().to_internal_value(data)


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
    post_id = serializers.IntegerField()
    author_id = serializers.IntegerField(
        required=True, help_text="Id of user that create post"
    )
    author_email = serializers.CharField()
    author_display_name = serializers.CharField()
    likes_count = serializers.IntegerField()
    is_liked_by_user = serializers.BooleanField(
        required=True, help_text="Is post liked by current authenticated user"
    )
    comments_count = serializers.IntegerField()

    # TODO: use UserResponseSerializer for author

    class Meta:
        model = Post
        fields = [
            "post_id",
            "author_id",
            "author_email",
            "author_display_name",
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


# # TODO
# def get_post_comments_example():
#     return {}

# # @extend_schema_serializer(
# #     examples=utils.single_example(get_post_response_example()),
# # )
# class GetPostCommentsSerializer(serializers.ModelSerializer, utils.StrictFieldsMixin):
#     post_id = serializers.IntegerField()
#     author_id = serializers.IntegerField(
#         required=True, help_text="Id of user that create post"
#     )
#     author_email = serializers.CharField()
#     author_name = serializers.CharField(required=False)
#     likes_count = serializers.IntegerField()
#     is_liked_by_user = serializers.BooleanField(
#         required=True, help_text="Is post liked by current authenticated user"
#     )
#     comments_count = serializers.IntegerField()

#     class Meta:
#         model = Post
#         fields = [
#             "post_id",
#             "author_id",
#             "author_email",
#             "author_name",
#             "title",
#             "text_content",
#             "created_at",
#             "edited_at",
#             "likes_count",
#             "is_liked_by_user",
#             "comments_count",
#         ]
#         extra_kwargs = {
#             "text_content": {"required": True},  # TODO: make it optional
#         }


class PostsV1SearchParamsSerializer(utils.StrictFieldsMixin):
    post_title_search_str = serializers.IntegerField(required=False)
