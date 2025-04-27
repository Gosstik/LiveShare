from django.urls import path

from users.views import UsersV1Search
from users.views import UserV1FriendsInviteApiView
from users.views import UserV1FriendsInviteCancelApiView
from users.views import UserV1FriendsInviteAcceptApiView
from users.views import UserV1FriendsInviteRejectApiView
from users.views import UserV1FriendsRemoveApiView


urlpatterns = [
    path("v1/search", UsersV1Search.as_view(), name="users-v1-search"),
    path("v1/friends/invite/<int:other_user_id>", UserV1FriendsInviteApiView.as_view(), name="v1-friends-invite"),
    path("v1/friends/invite/cancel/<int:other_user_id>", UserV1FriendsInviteCancelApiView.as_view(), name="v1-friends-invite-cancel"),
    path("v1/friends/invite/accept/<int:other_user_id>", UserV1FriendsInviteAcceptApiView.as_view(), name="v1-friends-invite-accept"),
    path("v1/friends/invite/reject/<int:other_user_id>", UserV1FriendsInviteRejectApiView.as_view(), name="v1-friends-invite-reject"),
    path("v1/friends/remove/<int:other_user_id>", UserV1FriendsRemoveApiView.as_view(), name="v1-friends-remove"),
]
