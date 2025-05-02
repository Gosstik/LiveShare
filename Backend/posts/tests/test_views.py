import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from posts.models import Post, PostLike
from posts.tests.conftest import annotate_post_queryset


@pytest.mark.django_db
class TestCreatePostApiView:
    def test_create_post(self, auth_client, post_data):
        response = auth_client.post("/posts/v1/post/create", post_data)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
        assert Post.objects.count() == 1
        post = Post.objects.first()
        assert post.title == post_data["title"]
        assert post.text_content == post_data["text_content"]

    @pytest.mark.skip(reason="TODO: Fix image validation in EditPostRequestSerializer")
    def test_create_post_with_image(self, auth_client, post_data):
        # Create a proper image file
        image_content = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
            b"\x00\x00\x00\nIDATx\x9cc\x00\x00\x00\x02\x00\x01\xe5\x27\xde\xfc\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        image = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )
        data = {**post_data, "attached_image": image}
        response = auth_client.post("/posts/v1/post/create", data, format="multipart")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        post = Post.objects.first()
        assert post.attached_image is not None

    def test_create_post_unauthorized(self, api_client, post_data):
        response = api_client.post("/posts/v1/post/create", post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_post_invalid_data(self, auth_client):
        response = auth_client.post("/posts/v1/post/create", {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetEditDeletePostApiView:
    def test_get_post(self, api_client, sample_post, request_with_user):
        post = annotate_post_queryset(
            Post.objects.filter(id=sample_post.id), request_with_user.user
        ).get()

        response = api_client.get(f"/posts/v1/post/{post.id}")
        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data["id"] == post.id
        assert response.data["title"] == post.title

    def test_get_nonexistent_post(self, api_client):
        response = api_client.get("/posts/v1/post/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_post(self, auth_client, sample_post):
        update_data = {"title": "Updated Title"}
        response = auth_client.patch(f"/posts/v1/post/{sample_post.id}", update_data)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        sample_post.refresh_from_db()
        assert sample_post.title == update_data["title"]

    def test_delete_post(self, auth_client, sample_post):
        response = auth_client.delete(f"/posts/v1/post/{sample_post.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(id=sample_post.id).exists()


@pytest.mark.django_db
class TestPostLikeUnlikeApiView:
    def test_like_post(self, auth_client, sample_post):
        response = auth_client.post(f"/posts/v1/post/{sample_post.id}/like")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert PostLike.objects.filter(post=sample_post).exists()

    def test_unlike_post(self, auth_client, sample_post, user):
        # Create like first
        PostLike.objects.create(post=sample_post, user=user)
        response = auth_client.post(f"/posts/v1/post/{sample_post.id}/unlike")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PostLike.objects.filter(post=sample_post).exists()

    def test_duplicate_like(self, auth_client, sample_post, user):
        # Create initial like
        PostLike.objects.create(post=sample_post, user=user)
        response = auth_client.post(f"/posts/v1/post/{sample_post.id}/like")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unlike_nonexistent_like(self, auth_client, sample_post):
        response = auth_client.post(f"/posts/v1/post/{sample_post.id}/unlike")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.skip(
    reason="TODO: Fix query parameter validation in GetPostsByFiltersApiView"
)
class TestGetPostsByFiltersApiView:
    def test_get_posts_no_filters(
        self, api_client, sample_post, request_with_user, query_params
    ):
        annotate_post_queryset(Post.objects.all(), request_with_user.user)
        response = api_client.get(
            "/posts/v1/by-filters?"
            + "&".join([f"{k}={v}" for k, v in query_params.items()])
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["posts"]) == 1
        assert response.data["posts"][0]["id"] == sample_post.id

    def test_filter_by_author(
        self, api_client, sample_post, user, request_with_user, query_params
    ):
        annotate_post_queryset(Post.objects.all(), request_with_user.user)
        query_params["author_id"] = user.id
        response = api_client.get(
            "/posts/v1/by-filters?"
            + "&".join([f"{k}={v}" for k, v in query_params.items()])
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["posts"]) == 1
        assert response.data["posts"][0]["author"]["id"] == user.id

    def test_filter_by_post_id(
        self, api_client, sample_post, request_with_user, query_params
    ):
        annotate_post_queryset(Post.objects.all(), request_with_user.user)
        query_params["post_id"] = sample_post.id
        response = api_client.get(
            "/posts/v1/by-filters?"
            + "&".join([f"{k}={v}" for k, v in query_params.items()])
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["posts"]) == 1
        assert response.data["posts"][0]["id"] == sample_post.id

    def test_search_by_title(
        self, api_client, sample_post, request_with_user, query_params
    ):
        annotate_post_queryset(Post.objects.all(), request_with_user.user)
        query_params["post_title_search_str"] = "Test"
        response = api_client.get(
            "/posts/v1/by-filters?"
            + "&".join([f"{k}={v}" for k, v in query_params.items()])
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["posts"]) == 1
        assert "Test" in response.data["posts"][0]["title"]

    def test_sort_by_created_at(
        self, api_client, sample_post, user, request_with_user, query_params
    ):
        # Create another post
        Post.objects.create(author=user, title="Another Post", text_content="Content")
        annotate_post_queryset(Post.objects.all(), request_with_user.user)
        response = api_client.get(
            "/posts/v1/by-filters?"
            + "&".join([f"{k}={v}" for k, v in query_params.items()])
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["posts"]) == 2
        # Verify descending order
        assert (
            response.data["posts"][0]["created_at"]
            > response.data["posts"][1]["created_at"]
        )
