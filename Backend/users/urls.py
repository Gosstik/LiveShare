from django.urls import path

from users.views import UsersV1Search
from users.views import UserV1FriendsInviteApiView
from users.views import UserV1FriendsRemoveApiView


urlpatterns = [
    path("v1/search", UsersV1Search.as_view(), name="tmp-create-test"),
    path("v1/friends/invite/<int:other_user_id>", UserV1FriendsInviteApiView.as_view(), name="v1-friends-invite"),
    path("v1/friends/invite/accept/<int:other_user_id>", UserV1FriendsInviteApiView.as_view(), name="v1-friends-invite-accept"),
    path("v1/friends/invite/reject/<int:other_user_id>", UserV1FriendsInviteApiView.as_view(), name="v1-friends-invite-reject"),
    path("v1/friends/remove/<int:other_user_id>", UserV1FriendsRemoveApiView.as_view(), name="v1-friends-remove"),
]
