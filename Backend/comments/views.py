from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes

import Backend.utils as utils
from custom_auth.mixins import OptionalAuthApiMixin
from posts.utils import get_post_or_404

from comments.models import Comment
from comments.models import CommentLike
from comments.utils import get_comment_or_404
from comments.utils import get_comments_for_post

from comments.serializers import CreateCommentRequestSerializer
from comments.serializers import EditCommentRequestSerializer
from comments.serializers import CommentsByFiltersParamsSerializer
from comments.serializers import CommentsForPostSerializer
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
        serializer = CreateCommentRequestSerializer(data=request.data, context={'request_user': request.user})
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


class CommentsForPostApiView(OptionalAuthApiMixin, APIView):
    @extend_schema(
        parameters=[CommentsByFiltersParamsSerializer],
        responses={
            status.HTTP_200_OK: CommentsForPostSerializer,
        },
    )
    def get(self, request: Request, post_id: int):
        # TODO: add pagination
        params = utils.validate_data(
            request.query_params,
            CommentsByFiltersParamsSerializer,
        )

        comments = get_comments_for_post(params, post_id, request.user)
        comments_data = transform_db_comments_for_response(comments)

        response_data = {
            "post_id": post_id,
            "comments": comments_data,
        }
        return utils.validate_and_get_response(
            response_data, CommentsForPostSerializer
        )


class CommentLikeApiView(APIView):
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


class CommentUnlikeApiView(APIView):
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
