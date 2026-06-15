from django.test import TestCase

from .models import AuditLog


class AuditLogModelTest(TestCase):
    def test_create_log(self):
        log = AuditLog.objects.create(
            action=AuditLog.Action.CREATE,
            resource_type="post",
            description="Post criado",
        )
        self.assertEqual(log.action, AuditLog.Action.CREATE)
