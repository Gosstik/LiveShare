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


class UsersSearchUserType(utils.EnumWithContains):
    ALL = "all"
    FRIENDS = "friends"


USERS_SEARCH_USER_TYPES = [(val.value, val.name) for val in UsersSearchUserType]
