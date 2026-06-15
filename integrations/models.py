import uuid

from django.conf import settings
from django.db import models

from .crypto import decrypt_token, encrypt_token


class SocialAccount(models.Model):
    class Platform(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        LINKEDIN = "linkedin", "LinkedIn"
        TWITTER = "twitter", "X (Twitter)"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="social_accounts",
        verbose_name="organização",
    )
    platform = models.CharField(
        "plataforma",
        max_length=20,
        choices=Platform.choices,
    )
    account_name = models.CharField("nome da conta", max_length=255)
    account_id = models.CharField("ID da conta", max_length=255)
    _access_token = models.TextField("token de acesso (criptografado)", db_column="access_token")
    _refresh_token = models.TextField(
        "token de refresh (criptografado)",
        db_column="refresh_token",
        blank=True,
    )
    token_expires_at = models.DateTimeField("token expira em", null=True, blank=True)
    metadata = models.JSONField("metadados", default=dict, blank=True)
    is_active = models.BooleanField("ativo", default=True)
    connected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="connected_accounts",
        verbose_name="conectado por",
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "conta social"
        verbose_name_plural = "contas sociais"
        unique_together = [("organization", "platform", "account_id")]
        ordering = ["platform", "account_name"]

    def __str__(self):
        return f"{self.get_platform_display()} — {self.account_name}"

    @property
    def access_token(self) -> str:
        return decrypt_token(self._access_token)

    @access_token.setter
    def access_token(self, value: str):
        self._access_token = encrypt_token(value)

    @property
    def refresh_token(self) -> str:
        if not self._refresh_token:
            return ""
        return decrypt_token(self._refresh_token)

    @refresh_token.setter
    def refresh_token(self, value: str):
        self._refresh_token = encrypt_token(value) if value else ""
