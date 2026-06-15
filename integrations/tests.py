from django.test import TestCase, override_settings
from cryptography.fernet import Fernet

from accounts.models import Organization
from .models import SocialAccount


@override_settings(SOCIAL_ENCRYPTION_KEY=Fernet.generate_key().decode())
class SocialAccountModelTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Test", slug="test")

    def test_token_encryption_roundtrip(self):
        account = SocialAccount(
            organization=self.org,
            platform=SocialAccount.Platform.FACEBOOK,
            account_name="Page Test",
            account_id="12345",
        )
        account.access_token = "secret-token"
        account.refresh_token = "refresh-token"
        account.save()

        reloaded = SocialAccount.objects.get(pk=account.pk)
        self.assertEqual(reloaded.access_token, "secret-token")
        self.assertEqual(reloaded.refresh_token, "refresh-token")
        self.assertNotEqual(reloaded._access_token, "secret-token")
