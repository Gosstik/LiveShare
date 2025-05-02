import pytest
from django.db.models import BooleanField, Case, Count, QuerySet, When
from rest_framework.test import APIClient, APIRequestFactory

from posts.models import Post
from users.models import User


def annotate_post_queryset(queryset: QuerySet, user) -> QuerySet:
    return queryset.annotate(
        likes_count=Count("postlike"),
        comments_count=Count("comment"),
        is_liked_by_user=Case(
            When(postlike__user=user, then=True),
            default=False,
            output_field=BooleanField(),
        ),
    )


@pytest.fixture(name="user")
def _user():
    return User.objects.create_user(
        email="test@example.com", password="testpass123", username="testuser"
    )


@pytest.fixture(name="another_user")
def _another_user():
    return User.objects.create_user(
        email="another@example.com", password="testpass123", username="anotheruser"
    )


@pytest.fixture(name="api_client")
def _api_client():
    return APIClient()


@pytest.fixture(name="auth_client")
def _auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(name="request_with_user")
def _request_with_user(user):
    factory = APIRequestFactory()
    request = factory.get("/")
    request.user = user
    return request


@pytest.fixture(name="post_data")
def _post_data():
    return {"title": "Test Title", "text_content": "Test Content"}


@pytest.fixture(name="sample_post")
def _sample_post(user):
    return Post.objects.create(
        author=user, title="Test Post", text_content="This is a test post content"
    )


@pytest.fixture(name="query_params")
def _query_params():
    return {"sort_field_name": "created_at", "sort_type": "desc"}
