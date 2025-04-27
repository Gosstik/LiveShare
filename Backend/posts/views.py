from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes

import Backend.utils as utils
from custom_auth.mixins import PublicApiMixin, AuthApiMixin

from posts.models import Post, PostLike
from posts.utils import get_post_or_404
from posts.utils import post_404_response
from posts.utils import get_posts_by_filters_from_db
from posts.utils import transform_db_posts_for_response

from posts.serializers import CreatePostRequestSerializer
from posts.serializers import EditPostRequestSerializer
from posts.serializers import GetPostResponseSerializer
from posts.serializers import GetPostsByFiltersResponseSerializer
from posts.serializers import GetPostsByFiltersParamsSerializer
from posts.serializers import PostsV1SearchParamsSerializer


class CreatePostApiView(APIView):
    @extend_schema(
        request=CreatePostRequestSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.SerializerErrorsSerializer,
        },
    )
    def post(self, request):
        serializer = CreatePostRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return utils.get_serializer_errors_response(serializer)


class GetEditDeletePostApiView(APIView):
    @extend_schema(
        responses=GetPostResponseSerializer,
    )
    def get(self, request: Request, post_id: int):
        params = utils.validate_data(
            {"post_id": post_id}, GetPostsByFiltersParamsSerializer
        )
        posts_data = get_posts_by_filters_from_db(params, request.user)
        response_posts_data = transform_db_posts_for_response(posts_data)
        if not response_posts_data:
            return post_404_response(post_id)
        serializer = GetPostResponseSerializer(response_posts_data[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=EditPostRequestSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.SerializerErrorsSerializer,
        },
    )
    def patch(self, request, post_id):
        instance = get_post_or_404(post_id)
        serializer = EditPostRequestSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return utils.get_serializer_errors_response(serializer)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="post_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="ID of the post to delete",
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            # TODO: add 404
        },
    )
    def delete(self, request, post_id):
        instance = get_post_or_404(post_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class DeletePostViewSetV1(
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = Post.objects.all()
#     serializer_class = CreatePostRequestSerializer
#     lookup_url_kwarg = "post_id"


class PostLikeApiView(APIView, AuthApiMixin):
    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def post(self, request, post_id):
        (_, was_created) = PostLike.objects.get_or_create(
            post_id=post_id,
            user=request.user,
        )
        if not was_created:
            return utils.basic_bad_request(
                code="like_already_exists",
                detail=f"Like already exists for post_id={post_id}, user_id={request.user.id}",
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostUnlikeApiView(APIView, AuthApiMixin):
    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def post(self, request, post_id):
        row = PostLike.objects.filter(
            post__id=post_id,
            user=request.user,
        )
        if not row.exists():
            return utils.basic_bad_request(
                code="like_not_found",
                detail=f"Like is not set, post_id={post_id}, user_id={request.user.id}",
            )
        row.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetPostsByFiltersApiView(APIView):
    @extend_schema(
        parameters=[
            GetPostsByFiltersParamsSerializer,
        ],
        responses={
            status.HTTP_200_OK: GetPostsByFiltersResponseSerializer,
            # TODO: add 500 in case of serializer error
        },
    )
    def get(self, request: Request):
        # TODO: support cursor
        params = utils.deserialize_or_400(
            request.query_params,
            GetPostsByFiltersParamsSerializer,
            detail="Request params deserialization failed",
        )

        # Create posts for response
        posts = get_posts_by_filters_from_db(params, request.user)
        response_data = {"posts": transform_db_posts_for_response(posts)}
        return utils.validate_and_get_response(
            response_data,
            GetPostsByFiltersResponseSerializer,
            raise_exception=True,
        )


class PostsV1SearchApiView(APIView):
    @extend_schema(
        parameters=[
            PostsV1SearchParamsSerializer,
        ],
        responses={
            status.HTTP_200_OK: GetPostsByFiltersResponseSerializer,
            # TODO: add 500 in case of serializer error
        },
    )
    def get(self, request: Request):
        # TODO: support cursor
        params = utils.deserialize_or_400(
            request.query_params,
            GetPostsByFiltersParamsSerializer,
            detail="Request params deserialization failed",
        )

        # Create posts for response
        posts = get_posts_by_filters_from_db(params, request.user)
        response_data = {"posts": transform_db_posts_for_response(posts)}
        return utils.validate_and_get_response(
            response_data,
            GetPostsByFiltersResponseSerializer,
            raise_exception=True,
        )
