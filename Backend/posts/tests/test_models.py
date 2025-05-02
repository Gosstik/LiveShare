import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.utils import timezone

from posts.models import Post, PostLike, PostView


@pytest.mark.django_db
class TestPostModel:
    def test_create_post_with_required_fields(self, user):
        post = Post.objects.create(
            author=user, title="Test Title", text_content="Test Content"
        )
        assert post.title == "Test Title"
        assert post.text_content == "Test Content"
        assert post.author == user
        assert post.created_at is not None
        assert post.edited_at is not None

    def test_create_post_with_image(self, user):
        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        post = Post.objects.create(
            author=user,
            title="Test Title",
            text_content="Test Content",
            attached_image=image,
        )
        assert post.attached_image.name.startswith("posts_attached_images/")
        assert post.attached_image_url.startswith(settings.BACKEND_BASE_URL)

    def test_post_str_representation(self, sample_post):
        expected = f"{sample_post.id}, {sample_post.author}: {sample_post.title}"
        assert str(sample_post) == expected

    def test_auto_update_edited_at(self, sample_post):
        original_edited_at = timezone.now()
        sample_post.title = "Updated Title"
        sample_post.save()
        assert sample_post.edited_at > original_edited_at

    def test_get_related_comments(self, sample_post):
        comments = sample_post.get_related_comments()
        assert hasattr(comments, "all")  # Verify it returns a QuerySet
        assert isinstance(comments, type(sample_post.comment_set.all()))


@pytest.mark.django_db
class TestPostLikeModel:
    def test_create_post_like(self, sample_post, user):
        post_like = PostLike.objects.create(post=sample_post, user=user)
        assert post_like.post == sample_post
        assert post_like.user == user

    def test_unique_constraint(self, sample_post, user):
        PostLike.objects.create(post=sample_post, user=user)
        with pytest.raises(IntegrityError):
            PostLike.objects.create(post=sample_post, user=user)

    def test_post_like_str_representation(self, sample_post, user):
        post_like = PostLike.objects.create(post=sample_post, user=user)
        expected = f"post_id={sample_post.id}, user={user}"
        assert str(post_like) == expected


@pytest.mark.django_db
class TestPostViewModel:
    def test_create_post_view(self, sample_post, user):
        post_view = PostView.objects.create(post=sample_post, user=user)
        assert post_view.post == sample_post
        assert post_view.user == user

    def test_unique_constraint(self, sample_post, user):
        PostView.objects.create(post=sample_post, user=user)
        with pytest.raises(IntegrityError):
            PostView.objects.create(post=sample_post, user=user)

    def test_post_view_str_representation(self, sample_post, user):
        post_view = PostView.objects.create(post=sample_post, user=user)
        expected = f"post_id={sample_post.id}, user={user}"
        assert str(post_view) == expected
