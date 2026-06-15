from django.test import TestCase

from accounts.models import CustomUser, Organization
from .models import Notification
from .services import create_notification


class NotificationServiceTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Test", slug="test")
        self.user = CustomUser.objects.create_user(
            username="notifyuser",
            password="pass",
            organization=self.org,
        )

    def test_create_notification(self):
        notif = create_notification(self.user, "Teste", "Mensagem de teste")
        self.assertEqual(notif.type, Notification.Type.INFO)
        self.assertFalse(notif.is_read)
