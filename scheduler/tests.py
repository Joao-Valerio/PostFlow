from django.test import TestCase

from accounts.models import CustomUser, Organization
from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Test", slug="test")
        self.user = CustomUser.objects.create_user(
            username="author",
            password="pass",
            organization=self.org,
        )

    def test_post_creation(self):
        post = Post.objects.create(
            organization=self.org,
            author=self.user,
            content="Hello world",
        )
        self.assertEqual(post.status, Post.Status.DRAFT)
        self.assertIn("Hello", str(post))
