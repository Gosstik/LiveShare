from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import mixins, viewsets

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes

import Backend.utils as utils
from custom_auth.mixins import PublicApiMixin, AuthApiMixin
from posts.utils import get_post_or_404

from comments.models import Comment
from comments.models import CommentLike
from comments.utils import get_comment_or_404
from comments.utils import make_comments_by_filters_query

from comments.serializers import CreateCommentRequestSerializer
from comments.serializers import EditCommentRequestSerializer
from comments.serializers import CommentsByFiltersParamsSerializer
from comments.serializers import CommentsByFilterSerializer
from comments.serializers import transform_db_comments_for_response


class CreateCommentApiView(APIView):
    @extend_schema(
        request=CreateCommentRequestSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.SerializerErrorsSerializer,
        },
    )
    def post(self, request):
        serializer = CreateCommentRequestSerializer(data=request.data)
        if serializer.is_valid():
            get_post_or_404(serializer.validated_data["post_id"])
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return utils.get_serializer_errors_response(serializer)


class EditDeleteCommentApiView(APIView):
    @extend_schema(
        request=EditCommentRequestSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: utils.SerializerErrorsSerializer,
        },
    )
    def patch(self, request, comment_id):
        instance = Comment.objects.get(id=comment_id)
        serializer = EditCommentRequestSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return utils.get_serializer_errors_response(
            serializer, detail="Failed to deserialize request data"
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="comment_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                required=True,
                description="ID of the comment to delete",
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            # TODO: add 404
        },
    )
    def delete(self, request, comment_id):
        instance = get_comment_or_404(comment_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_comments_data(post_id: int, request: Request):
    # TODO: add filters
    comments = Comment.objects.filter(
        post__id=post_id,
    )

    comments_data = []
    for comment in comments:
        # TODO: make one sql query
        likes = list(CommentLike.objects.filter(comment__id=comment.id))

        if request.user.is_authenticated:
            is_liked_by_user = any((like.user.id == request.user.id for like in likes))
        else:
            is_liked_by_user = False

        # TODO: add user profile image
        author_display_name = utils.get_user_display_name(
            comment.author.email,
            comment.author.first_name,
            comment.author.last_name,
        )
        comment_data = {
            "comment_id": comment.id,
            "author_id": comment.author.id,
            "author_email": comment.author.email,
            "author_display_name": author_display_name,
            "text_content": comment.text_content,
            "created_at": comment.created_at,
            "edited_at": comment.edited_at,
            "likes_count": len(likes),
            "is_liked_by_user": is_liked_by_user,
        }
        utils.validate_data(comment_data, CommentsByFilterSerializer)
        comments_data.append(comment_data)

    return comments_data


class CommentsByPostApiView(APIView):
    # TODO: add pagination
    @extend_schema(
        parameters=[CommentsByFiltersParamsSerializer],
        responses={
            status.HTTP_200_OK: CommentsByFilterSerializer,
        },
    )
    def get(self, request):
        # TODO: get params
        # Get and validate query params
        params_serializer = CommentsByFiltersParamsSerializer(data=request.query_params)
        if not params_serializer.is_valid():
            return utils.get_serializer_errors_response(
                params_serializer, detail="Request params deserialization failed"
            )
        params = params_serializer.validated_data

        # Make db query
        comments = make_comments_by_filters_query(params, request.user)
        comments_data = transform_db_comments_for_response(comments)

        # TODO: transforming

        # Create response
        # comments_data = []
        # for comment in comments:
        #     author_display_name = utils.get_user_display_name(
        #         comment.author.email,
        #         comment.author.first_name,
        #         comment.author.last_name,
        #     )

        #     # TODO: add user profile image
        #     comment_data = {
        #         "comment_id": comment.id,
        #         "author_id": comment.author.id,
        #         "author_email": comment.author.email,
        #         "author_display_name": author_display_name,
        #         "text_content": comment.text_content,
        #         "created_at": comment.created_at,
        #         "edited_at": comment.edited_at,
        #         "likes_count": comment.likes_count,
        #         "is_liked_by_user": comment.is_liked_by_user,
        #     }
        #     utils.validate_data(
        #         comment_data,
        #         CommentByFiltersSerializer,
        #         verbose_code=f"Validation for comment_id={comment.id}",
        #     )
        #     comments_data.append(comment_data)


        ### Old flow
        response_data = {
            "post_id": params["post_id"],
            # "comments": get_comments_data(params['post_id'], request),
            "comments": comments_data,
        }
        # TODO:
        return utils.validate_and_get_response(
            response_data, CommentsByFilterSerializer
        )


class CommentLikeApiView(APIView, AuthApiMixin):
    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def post(self, request, comment_id):
        (_, was_created) = CommentLike.objects.get_or_create(
            comment_id=comment_id,
            user=request.user,
        )
        if not was_created:
            return utils.basic_bad_request(
                code="like_already_exists",
                detail=f"Like already exists for comment_id={comment_id}, user_id={request.user.id}",
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentUnlikeApiView(APIView, AuthApiMixin):
    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def post(self, request, comment_id):
        row = CommentLike.objects.filter(
            comment__id=comment_id,
            user=request.user,
        )
        if not row.exists():
            return utils.basic_bad_request(
                code="like_not_found",
                detail=f"Like is not set, comment_id={comment_id}, user_id={request.user.id}",
            )
        row.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
