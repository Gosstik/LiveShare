from django.urls import path

from users.views import UsersV1Search
from users.views import UserV1FriendsInviteApiView
from users.views import UserV1FriendsRemoveApiView


urlpatterns = [
    path("v1/search", UsersV1Search.as_view(), name="tmp-create-test"),
    path("v1/<int:user_id>/friends/invite", UserV1FriendsInviteApiView.as_view(), name="v1-friends-invite"),
    path("v1/<int:user_id>/friends/remove", UserV1FriendsRemoveApiView.as_view(), name="v1-friends-remove"),
]
