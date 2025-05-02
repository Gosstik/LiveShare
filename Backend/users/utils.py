from django.db.models import Case, CharField, Exists, OuterRef, Value, When

import Backend.utils as utils
from users.models import FriendInvitation, Friends, User


class UsersSearchUserType(utils.EnumWithContains):
    ALL = "all"
    FRIENDS = "friends"


class UserFriendStatus(utils.EnumWithContains):
    FRIEND = "friend"
    RECEIVED_INVITATION = "received_invitation"
    SENT_INVITATION = "sent_invitation"
    NOT_FRIEND = "not_friend"


USERS_SEARCH_USER_TYPES = [(val.value, val.name) for val in UsersSearchUserType]
USER_FRIEND_STATUSES = [(val.value, val.name) for val in UserFriendStatus]


def create_friends(user_1_id: int, user_2_id: int):
    Friends.objects.bulk_create(
        [
            Friends(user_id=user_1_id, friend_id=user_2_id),
            Friends(user_id=user_2_id, friend_id=user_1_id),
        ]
    )


def _get_users_with_friend_status(auth_user: User):
    # Create subqueries to check existence
    is_friend = Friends.objects.filter(user=auth_user, friend=OuterRef("pk"))

    received_invitation = FriendInvitation.objects.filter(
        from_user=OuterRef("pk"), to_user=auth_user
    )

    sent_invitation = FriendInvitation.objects.filter(
        from_user=auth_user, to_user=OuterRef("pk")
    )

    # Annotate users with friend_status
    users = User.objects.exclude(id=auth_user.id).annotate(
        friend_status=Case(
            When(Exists(is_friend), then=Value(UserFriendStatus.FRIEND)),
            When(
                Exists(received_invitation),
                then=Value(UserFriendStatus.RECEIVED_INVITATION),
            ),
            When(Exists(sent_invitation), then=Value(UserFriendStatus.SENT_INVITATION)),
            default=Value(UserFriendStatus.NOT_FRIEND),
            output_field=CharField(),
        )
    )

    return users


def get_users_by_filters(request_user: User, params):
    if params["users_type"] == UsersSearchUserType.FRIENDS:
        utils.true_or_400(
            request_user.is_authenticated,
            code="invalid_filters",
            detail="Unauthorized request to list friends",
        )
        result_users = _get_users_with_friend_status(request_user)
        friend_ids = Friends.objects.filter(user=request_user).values_list(
            "friend_id", flat=True
        )
        return result_users.filter(id__in=friend_ids)
    elif request_user.is_authenticated:
        return _get_users_with_friend_status(request_user)

    return User.objects.all()
