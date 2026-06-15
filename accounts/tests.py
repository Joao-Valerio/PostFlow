from django.test import TestCase

from .models import CustomUser, Organization


class OrganizationModelTest(TestCase):
    def test_str_returns_name(self):
        org = Organization.objects.create(name="Acme Corp", slug="acme-corp")
        self.assertEqual(str(org), "Acme Corp")


class CustomUserModelTest(TestCase):
    def test_user_with_organization(self):
        org = Organization.objects.create(name="Test Org", slug="test-org")
        user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass123",
            organization=org,
            role=CustomUser.Role.ADMIN,
        )
        self.assertTrue(user.is_org_admin)
        self.assertEqual(user.organization, org)
