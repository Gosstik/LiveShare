import datetime as dt

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from comments.models import Comment, CommentLike
from posts.models import Post, PostLike
from users.models import FriendInvitation, Friends

User = get_user_model()

# Base time for creating posts and comments (7 days ago)
BASE_TIME = timezone.now() - dt.timedelta(days=7)

LONG_TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute 
irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste 
natus error sit voluptatem accusantium doloremque laudantium.
"""

LONG_COMMENT = """
Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium 
doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore 
veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam 
voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur 
magni dolores eos qui ratione voluptatem sequi nesciunt.
"""


class Command(BaseCommand):
    help = "Creates development data from fixtures"

    def _clear_all_data(self):
        """Clear all existing data from the database"""
        self.stdout.write("Clearing existing data...")

        # Clear data using Django ORM
        CommentLike.objects.all().delete()
        Comment.objects.all().delete()
        PostLike.objects.all().delete()
        Post.objects.all().delete()
        FriendInvitation.objects.all().delete()
        Friends.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Successfully cleared all data"))

    def _load_fixture_data(self):
        """Load data from fixtures"""
        self.stdout.write("Creating fixture data...")

        # Create users
        users = []
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
            first_name="Admin",
            last_name="User",
        )
        users.append(admin)

        for i in range(4):
            user = User.objects.create_user(
                username=f"user{i + 1}",
                email=f"user{i + 1}@example.com",
                password=f"user{i + 1}",  # Password same as username
                first_name=f"User{i + 1}",
                last_name=f"LastName{i + 1}",
            )
            users.append(user)

        # Create friends relationships for user1 (users[1])
        Friends.objects.create(user=users[1], friend=users[2])  # user1 -> user2
        Friends.objects.create(user=users[2], friend=users[1])  # user2 -> user1
        Friends.objects.create(user=users[1], friend=users[3])  # user1 -> user3
        Friends.objects.create(user=users[3], friend=users[1])  # user3 -> user1

        # Create friend invitations
        FriendInvitation.objects.create(
            from_user=users[4], to_user=users[1]
        )  # user4 -> user1
        FriendInvitation.objects.create(
            from_user=users[3], to_user=users[2]
        )  # user3 -> user2

        # Create posts
        posts = []
        for i in range(7):
            author = users[i % len(users)]
            content = LONG_TEXT if i == 0 else f"This is the content of post {i + 1}"
            # Create posts with different timestamps
            # Post 0: 7 days ago
            # Post 1: 5 days ago
            # Post 2: 3 days ago
            # Post 3: 1 day ago
            # Post 4-6: Within last 24 hours, few hours apart
            if i < 4:
                created_time = BASE_TIME + dt.timedelta(days=i * 2)
            else:
                hours = (i - 4) * 3  # 3 hours apart
                created_time = timezone.now() - dt.timedelta(hours=hours)

            post = Post.objects.create(
                author=author,
                title=f"[{author.displayed_name}] Post {i + 1}",
                text_content=content,
                created_at=created_time,
                edited_at=created_time,
            )
            posts.append(post)

        # Create post likes
        # Post with 3 likes
        PostLike.objects.create(post=posts[0], user=users[1])
        PostLike.objects.create(post=posts[0], user=users[2])
        PostLike.objects.create(post=posts[0], user=users[3])

        # Some posts with 1-2 likes
        PostLike.objects.create(post=posts[1], user=users[2])
        PostLike.objects.create(post=posts[2], user=users[1])
        PostLike.objects.create(post=posts[2], user=users[3])

        # Create comments
        # Post with 4 comments
        comments = []
        for i in range(4):
            author = users[i % len(users)]
            content = LONG_COMMENT if i < 2 else f"Comment {i + 1} on post 1"
            # Create comments few minutes apart from post creation
            created_time = posts[0].created_at + dt.timedelta(minutes=i * 15)
            comment = Comment.objects.create(
                post=posts[0],
                author=author,
                text_content=f"[{author.displayed_name}] {content}",
                created_at=created_time,
                edited_at=created_time,
            )
            comments.append(comment)

        # Posts with 1-2 comments (posts[1] through posts[4])
        for i in range(1, 5):
            author = users[(i + 1) % len(users)]
            # Create comments 30 minutes after post creation
            created_time = posts[i].created_at + dt.timedelta(minutes=30)
            comment = Comment.objects.create(
                post=posts[i],
                author=author,
                text_content=f"[{author.displayed_name}] Comment on post {i + 1}",
                created_at=created_time,
                edited_at=created_time,
            )
            comments.append(comment)
            if i < 3:  # Add second comment for first two posts
                author = users[(i + 2) % len(users)]
                # Create second comment 15 minutes after first comment
                created_time = created_time + dt.timedelta(minutes=15)
                comment = Comment.objects.create(
                    post=posts[i],
                    author=author,
                    text_content=f"[{author.displayed_name}] Second comment on post {i + 1}",
                    created_at=created_time,
                    edited_at=created_time,
                )
                comments.append(comment)

        # Create comment likes
        CommentLike.objects.create(comment=comments[0], user=users[1])
        CommentLike.objects.create(comment=comments[0], user=users[2])
        CommentLike.objects.create(comment=comments[1], user=users[3])
        CommentLike.objects.create(comment=comments[2], user=users[4])

        self.stdout.write(self.style.SUCCESS("Successfully created fixture data"))

    def handle(self, *args, **options):
        with transaction.atomic():
            self._clear_all_data()
            self._load_fixture_data()
