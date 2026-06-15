import uuid

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "create", "Criação"
        UPDATE = "update", "Atualização"
        DELETE = "delete", "Exclusão"
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        PUBLISH = "publish", "Publicação"
        CONNECT = "connect", "Conexão OAuth"
        OTHER = "other", "Outro"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="usuário",
    )
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="organização",
    )
    action = models.CharField("ação", max_length=20, choices=Action.choices)
    resource_type = models.CharField("tipo de recurso", max_length=100, blank=True)
    resource_id = models.CharField("ID do recurso", max_length=255, blank=True)
    description = models.TextField("descrição", blank=True)
    metadata = models.JSONField("metadados", default=dict, blank=True)
    ip_address = models.GenericIPAddressField("endereço IP", null=True, blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "log de auditoria"
        verbose_name_plural = "logs de auditoria"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_action_display()} — {self.resource_type} ({self.created_at})"
