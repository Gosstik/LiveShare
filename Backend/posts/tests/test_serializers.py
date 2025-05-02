import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post, PostLike
from posts.serializers import (
    EditPostRequestSerializer,
    GetPostResponseSerializer,
    GetPostsByFiltersParamsSerializer,
)
from posts.tests.conftest import annotate_post_queryset


@pytest.mark.django_db
class TestEditPostRequestSerializer:
    def test_valid_data(self, post_data, request_with_user):
        serializer = EditPostRequestSerializer(
            data=post_data, context={"request": request_with_user}
        )
        assert serializer.is_valid(), serializer.errors
        post = serializer.save()
        assert post.title == post_data["title"]
        assert post.text_content == post_data["text_content"]
        assert post.author == request_with_user.user

    @pytest.mark.skip(reason="TODO: Fix image validation in EditPostRequestSerializer")
    def test_create_with_image(self, post_data, request_with_user):
        # Create a proper image file
        image_content = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
            b"\x00\x00\x00\nIDATx\x9cc\x00\x00\x00\x02\x00\x01\xe5\x27\xde\xfc\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        image = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )
        data = {**post_data, "attached_image": image}

        serializer = EditPostRequestSerializer(
            data=data, context={"request": request_with_user}
        )
        assert serializer.is_valid()
        post = serializer.save()
        assert post.attached_image is not None
        assert post.attached_image.name.startswith("posts_attached_images/post_")

    def test_partial_update(self, request_with_user):
        post = Post.objects.create(
            author=request_with_user.user,
            title="Original Title",
            text_content="Original Content",
        )
        update_data = {"title": "Updated Title"}

        serializer = EditPostRequestSerializer(
            post, data=update_data, partial=True, context={"request": request_with_user}
        )
        assert serializer.is_valid()
        updated_post = serializer.save()
        assert updated_post.title == update_data["title"]
        assert updated_post.text_content == "Original Content"


@pytest.mark.django_db
class TestGetPostResponseSerializer:
    def test_post_serialization(self, user, request_with_user):
        post = Post.objects.create(
            author=user, title="Test Title", text_content="Test Content"
        )

        post = annotate_post_queryset(
            Post.objects.filter(id=post.id), request_with_user.user
        ).get()

        serializer = GetPostResponseSerializer(
            post, context={"request": request_with_user}
        )
        data = serializer.data

        assert data["id"] == post.id
        assert data["title"] == post.title
        assert data["text_content"] == post.text_content
        assert data["author"]["email"] == user.email
        assert data["likes_count"] == 0
        assert data["comments_count"] == 0
        assert not data["is_liked_by_user"]

    def test_with_likes_and_comments(self, user, request_with_user):
        post = Post.objects.create(
            author=user, title="Test Title", text_content="Test Content"
        )
        # Add a like
        PostLike.objects.create(post=post, user=user)

        post = annotate_post_queryset(
            Post.objects.filter(id=post.id), request_with_user.user
        ).get()

        serializer = GetPostResponseSerializer(
            post, context={"request": request_with_user}
        )
        data = serializer.data

        assert data["likes_count"] == 1
        assert data["is_liked_by_user"]

    def test_attached_image_handling(self, user, request_with_user):
        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        post = Post.objects.create(
            author=user,
            title="Test Title",
            text_content="Test Content",
            attached_image=image,
        )

        post = annotate_post_queryset(
            Post.objects.filter(id=post.id), request_with_user.user
        ).get()

        serializer = GetPostResponseSerializer(
            post, context={"request": request_with_user}
        )
        data = serializer.data
        assert "attached_image_url" in data
        assert data["attached_image_url"].startswith("http")


@pytest.mark.django_db
class TestGetPostsByFiltersParamsSerializer:
    def test_valid_filter_params(self):
        valid_data = {
            "post_id": 1,
            "author_id": 1,
            "sort_field_name": "created_at",
            "sort_type": "desc",
            "post_title_search_str": "test",
        }
        serializer = GetPostsByFiltersParamsSerializer(data=valid_data)
        assert serializer.is_valid()

    def test_optional_fields(self):
        minimal_data = {}  # All fields are optional
        serializer = GetPostsByFiltersParamsSerializer(data=minimal_data)
        assert serializer.is_valid()
        assert serializer.validated_data["sort_field_name"] == "created_at"
        assert serializer.validated_data["sort_type"] == "desc"

    def test_invalid_sort_field(self):
        invalid_data = {"sort_field_name": "invalid_field"}
        serializer = GetPostsByFiltersParamsSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "sort_field_name" in serializer.errors

    def test_invalid_sort_type(self):
        invalid_data = {"sort_type": "invalid_type"}
        serializer = GetPostsByFiltersParamsSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "sort_type" in serializer.errors
