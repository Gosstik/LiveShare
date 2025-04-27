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
    return {
        "title": "Test post title",
        "text_content": "Text content",
        # "attached_image": None, # TODO: ???
    }


@extend_schema_serializer(
    examples=utils.single_example(edit_post_request_example()),
)
class EditPostRequestSerializer(serializers.ModelSerializer, utils.StrictFieldsMixin):
    attached_image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["title", "text_content", "attached_image"]

    def create(self, validated_data):
        request = self.context.get('request')
        attached_image = None
        if 'attached_image' in validated_data:
            attached_image = validated_data.pop('attached_image')

        if request and request.user:
            validated_data['author'] = request.user

        post = Post.objects.create(**validated_data)

        if attached_image:
            # Generate filename using post ID
            ext = attached_image.name.split('.')[-1]
            attached_image.name = f'post_{post.id}.{ext}'
            post.attached_image = attached_image
            post.save()

        return post


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
    attached_image_url = serializers.CharField(required=False)

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
            "attached_image_url",
        ]
        extra_kwargs = {
            "text_content": {"required": True},  # TODO: make it optional
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Check if instance is a Post object (not a dict/ReturnDict)
        if hasattr(instance, 'attached_image') and instance.attached_image:
            representation['attached_image_url'] = instance.attached_image_url
        # Remove all None values from the output
        for field in self.fields.keys():
            if representation.get(field) is None:
                representation.pop(field, None)
        return representation


# TODO
def get_posts_by_filters_response_example():
    return {}


# @extend_schema_serializer(
#     examples=utils.single_example(get_post_response_example()),
# )
class GetPostsByFiltersResponseSerializer(utils.StrictFieldsMixin):
    posts = GetPostResponseSerializer(many=True)
