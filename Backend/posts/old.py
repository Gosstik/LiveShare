import json
import datetime as dt

from rest_framework import ISO_8601
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, viewsets

from custom_auth.utils import PublicApiMixin, AuthApiMixin
import Backend.utils as utils

from posts.models import Post, PostLike
from comments.models import Comment

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_serializer
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiTypes
from drf_spectacular.utils import OpenApiExample

#####

from rest_framework import serializers


#############################################
### Posts

### Viewsets
# /posts/v1/post/set/like      # add by custom action
# /posts/v1/post/comments

### APIView
# /posts/v1/get-by-filters

################################################################################

### Serializers


class PostViewSetV1Serializer(serializers.ModelSerializer):
    # id = models.BigAutoField(primary_key=True)

    # note = models.TextField(blank=True)
    # image = models.ImageField(upload_to="images/posts", blank=True)
    # post_id = serializers.IntegerField(
    #     read_only=True,
    # )
    author_id = serializers.IntegerField(
        required=True, help_text="Id of user that create post"
    )
    # TODO: add image and make it nullable
    text_content = serializers.CharField(
        required=True,
    )
    # created_at = serializers.DateTimeField(
    #     required=False, help_text="Datetime of post creation"
    # )
    # updated_at = serializers.DateTimeField(
    #     required=False, help_text="Datetime of changing post data"
    # )

    class Meta:
        model = Post
        fields = ["id", "author_id", "title", "text_content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        utils.set_default_help_text_from_model(self)


class PostViewSetV1ModifySerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required = True, read_only = True)
    author_id = serializers.IntegerField(
        required=True, help_text="Id of user that create post"
    )
    # TODO: add image and make it nullable
    text_content = serializers.CharField(
        required=True,
    )
    created_at = serializers.DateTimeField(
        required=True, help_text="Datetime of post creation"
    )
    updated_at = serializers.DateTimeField(
        required=True, help_text="Datetime of changing post data"
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author_id",
            "title",
            "text_content",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        print("****************************************")
        if self.context["request"].method == "GET":
            serializer = PostViewSetV1Serializer(instance)
            return serializer.data
        return super().to_representation(instance)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        utils.set_default_help_text_from_model(self)


class PostLikeViewSetV1Serializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"


################################################################################

# from drf_yasg.utils import swagger_auto_schema
# from django.utils.decorators import method_decorator

# class UserCurrent(views.APIView):
#   def get(self, request):
#     serializer = UserSerializer(request.user)
#     return response.Response(serializer.data)

# class PostAPIView(views.APIView)):
#     pass


class PostViewSetV1(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,  # TODO: we need more: likes and comments count
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,  # TODO: we must delete comments with it (check cascade works)
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all()  # .order_by("-date_joined")
    # serializer_class = PostViewSetV1Serializer
    swagger_schema = utils.NoTitleAutoSchema
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["post", "get", "patch"]

    def get_serializer_class(self):
        serializers = {
            "create": PostViewSetV1Serializer,
            "update": PostViewSetV1ModifySerializer,
            "partial_update": PostViewSetV1ModifySerializer,
            "retrieve": PostViewSetV1ModifySerializer,
            "delete": PostViewSetV1Serializer,
        }
        print(f"!!! self.action={self.action}")
        return serializers.get(self.action)
        # if self.action == 'create':
        #     return PostViewSetV1Serializer
        # return PostViewSetV1Serializer

    def perform_update(self, serializer):
        serializer.save(updated_at=dt.datetime.now())


# def perform_create(self, serializer):
#     queryset = SignupRequest.objects.filter(user=self.request.user)
#     if queryset.exists():
#         raise ValidationError('You have already signed up')
#     serializer.save(user=self.request.user)

### Filter
# def get_queryset(self):
#     user = self.request.user
#     return user.accounts.all()

# class CreatePostViewSet(mixins.CreateModelMixin,
#                         viewsets.GenericViewSet):
#     queryset = Post.objects.all()  # .order_by("-date_joined")
#     # serializer_class = PostViewSetV1Serializer
#     swagger_schema = utils.NoTitleAutoSchema
#     # permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)

#         post = Post.objects.get(id=request.data["post_id"])
#         # TODO: add likes
#         # posts = Posts.objects.all()

#         # response_arr = []
#     pass


def generate_example(serializer_class, valid_data):
    serializer = serializer_class(data=valid_data)
    serializer.is_valid(raise_exception=True)
    return serializer.data


# @extend_schema_serializer(
#     examples=[
#         generate_example(
#             CreatePostRequestSerializer,
#             {"my_example": 1},
#             summary="Create post example",
#             description="Example payload for creating a post",
#             request_only=True
#         )
#     ]
# )
# class CreatePostRequestSerializer(serializers.Serializer):
#     my_example = serializers.IntegerField()


def create_post_request_example():
    return {"author_id": 1, "title": "Test post title", "text_content": "Text content"}


@extend_schema_serializer(
    examples=single_example(create_post_request_example()),
)
class CreatePostRequestSerializer(serializers.ModelSerializer):
    # id = models.BigAutoField(primary_key=True)

    # note = models.TextField(blank=True)
    # image = models.ImageField(upload_to="images/posts", blank=True)
    # post_id = serializers.IntegerField(
    #     read_only=True,
    # )

    author_id = serializers.IntegerField(
        required=True, help_text="Id of user that create post"
    )
    # # TODO: add image and make it required=False (just delete)
    text_content = serializers.CharField(
        required=True,
    )

    # created_at = serializers.DateTimeField(
    #     required=False, help_text="Datetime of post creation"
    # )
    # updated_at = serializers.DateTimeField(
    #     required=False, help_text="Datetime of changing post data"
    # )

    class Meta:
        model = Post
        fields = ["author_id", "title", "text_content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        utils.set_default_help_text_from_model(self)


# CreatePostRequestSerializer = extend_schema_serializer(
#     examples=[
#         OpenApiExample(
#             name="Create post example",
#             # summary="Example payload",
#             # description="Example for creating post",
#             value={"my_example": 1},
#             request_only=True,
#         )
#     ]
# )(CreatePostRequestSerializer)


class CreatePostApiView(APIView):
    @extend_schema(
        # description="Basic creation",
        # parameters=[
        #   QuerySerializer,  # serializer fields are converted to parameters
        #   OpenApiParameter("nested", QuerySerializer),  # serializer object is converted to a parameter
        #   OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        #   OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH), # path variable was overridden
        # ],
        request=CreatePostRequestSerializer,
        # responses=CreatePostRequestSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
        # more customizations
        # examples=[
        #     OpenApiExample(
        #         "204",
        #         status_codes=["204"],
        #         summary="My documentation summary",
        #         description="My documentation description",
        #         request_only=True,
        #         value={
        #             "my_example": 1
        #         }
        #         # response_only=True,
        #     ),
        # ],
    )
    def post(self, request):
        # serializer = SnippetSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreatePostRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # post = Post.objects.get(id=request.data["post_id"])
        # Post.save(request.data)

        # # TODO: add likes
        # # posts = Posts.objects.all()
        # return Response(status.HTTP_204_NO_CONTENT)

        # response_arr = []

    pass

    # def ge

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save()

    # def get_success_headers(self, data):
    #     try:
    #         return {'Location': str(data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         return {}


class GetPostAPIView(APIView):
    def get(self, request):
        post = Post.objects.get(id=request.data["post_id"])
        # TODO: add likes
        # posts = Posts.objects.all()

        # response_arr = []

    def get_serializer_class():
        pass

    pass


class PostLikeViewSetV1(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = PostLike.objects.all()  # .order_by("-date_joined")
    serializer_class = PostLikeViewSetV1Serializer
    # permission_classes = [permissions.IsAuthenticated]


class DeletePostLike(APIView, PublicApiMixin):
    def delete(self, request):
        post = Post.objects.get(
            user=request.data["user_id"],
            post=request.data["post_id"],
        )
        # posts = Posts.objects.all()

        # response_arr = []
        # for post in posts:
        #     likes = list(PostLikes.objects.filter(post__id=post.id))
        #     comments_count = Comments.objects.filter(post__id=post.id).count()

        #     post_data = {
        #         "post_id": post.id,
        #         "author_email": post.author.email,
        #         "title": post.title,
        #         "text": post.note,
        #         "created_at": post.created_at,
        #         "likes_count": len(likes),
        #         "comments_count": comments_count,
        #     }
        #     if request.user.is_authenticated:
        #         post_data["is_liked_by_user"] = any(
        #             (like.user.email == request.user.email for like in likes)
        #         )

        #     response_arr.append(post_data)

        # response = {
        #     "posts": response_arr,
        # }

        # return Response(response, status=status.HTTP_200_OK)


class SetComment(APIView, PublicApiMixin):
    pass


# TODO: swagger definition
#    @swagger_auto_schema(
#         operation_description="POST description override using
#             decorator",
#         operation_summary="this is the summary from decorator",


#         # request_body is used to specify parameters
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=['name'],
#             properties={
#                 'name': openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#         tags=['my custom tag']
#     )
# TODO: add filter by post id
class GetAllPosts(APIView, PublicApiMixin):
    def get(self, request):
        posts = Post.objects.all()

        response_arr = []
        for post in posts:
            likes = list(PostLike.objects.filter(post__id=post.id))
            comments_count = Comment.objects.filter(post__id=post.id).count()

            post_data = {
                "post_id": post.id,
                "author_email": post.author.email,
                "title": post.title,
                "text": post.text_content,
                "created_at": post.created_at,
                "likes_count": len(likes),
                "comments_count": comments_count,
            }
            if request.user.is_authenticated:
                post_data["is_liked_by_user"] = any(
                    (like.user.email == request.user.email for like in likes)
                )

            response_arr.append(post_data)

        response = {
            "posts": response_arr,
        }

        return Response(response, status=status.HTTP_200_OK)


class UpdatePostLikes(APIView, AuthApiMixin):
    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        post_id = body.get("post_id")
        set_like = body.get("set_like")

        if post_id is None:
            return Response(
                {"error": "post_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if set_like is None:
            return Response(
                {"error": "set_like is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_like_count = PostLike.objects.filter(
            post_id=post_id,
            user=request.user,
        ).count()  # TODO: it is unique
        if user_like_count > 1:
            return Response(
                {
                    "error": f"User can like post only once, but stored {user_like_count} times"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        is_user_like_set = user_like_count == 1

        if set_like:
            if not is_user_like_set:
                PostLike.objects.create(
                    post_id=post_id,
                    user=request.user,
                )
        else:
            if is_user_like_set:
                PostLike.objects.filter(
                    post__id=post_id,
                    user=request.user,
                ).delete()

        return Response({}, status=status.HTTP_200_OK)


# TODO: delete post by id
# TODO: update post by id
