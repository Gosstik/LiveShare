from django.urls import path

from users.views import (
    UsersV1Search,
    UserV1FriendsApiView,
    UserV1FriendsInviteAcceptApiView,
    UserV1FriendsInviteApiView,
    UserV1FriendsInviteRejectApiView,
)

urlpatterns = [
    path("v1/search", UsersV1Search.as_view(), name="users-v1-search"),
    path(
        "v1/friends/<int:other_user_id>",
        UserV1FriendsApiView.as_view(),
        name="v1-friends",
    ),
    path(
        "v1/friends/invite/<int:other_user_id>",
        UserV1FriendsInviteApiView.as_view(),
        name="v1-friends-invite",
    ),
    path(
        "v1/friends/invite/accept/<int:other_user_id>",
        UserV1FriendsInviteAcceptApiView.as_view(),
        name="v1-friends-invite-accept",
    ),
    path(
        "v1/friends/invite/reject/<int:other_user_id>",
        UserV1FriendsInviteRejectApiView.as_view(),
        name="v1-friends-invite-reject",
    ),
]
