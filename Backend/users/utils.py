from django.db import transaction
from django.db.models import OuterRef
from django.db.models import Count
from django.db.models import Exists
from django.db.models import Subquery
from django.db.models import Value as V
from django.db.models.functions import Coalesce

import Backend.utils as utils
from Backend.exceptions import NotFound404
from users.models import User
from comments.models import Comment

from posts.models import Post
from posts.models import PostLike

from users.models import User
from users.models import Friends


class UsersSearchUserType(utils.EnumWithContains):
    ALL = "all"
    FRIENDS = "friends"


USERS_SEARCH_USER_TYPES = [(val.value, val.name) for val in UsersSearchUserType]


def create_friends(user_1_id: int, user_2_id: int):
    Friends.objects.bulk_create([
        Friends(user_id=user_1_id, friend_id=user_2_id),
        Friends(user_id=user_2_id, friend_id=user_1_id),
    ])
