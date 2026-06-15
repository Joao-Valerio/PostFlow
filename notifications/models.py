import uuid

from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Type(models.TextChoices):
        SUCCESS = "success", "Sucesso"
        FAILURE = "failure", "Falha"
        INFO = "info", "Informação"
        WARNING = "warning", "Aviso"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="usuário",
    )
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="organização",
        null=True,
        blank=True,
    )
    type = models.CharField("tipo", max_length=20, choices=Type.choices, default=Type.INFO)
    title = models.CharField("título", max_length=255)
    message = models.TextField("mensagem")
    is_read = models.BooleanField("lida", default=False)
    metadata = models.JSONField("metadados", default=dict, blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "notificação"
        verbose_name_plural = "notificações"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
