import uuid

from django.conf import settings
from django.db import models


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        SCHEDULED = "scheduled", "Agendado"
        PUBLISHING = "publishing", "Publicando"
        PUBLISHED = "published", "Publicado"
        FAILED = "failed", "Falhou"
        CANCELLED = "cancelled", "Cancelado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="organização",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="autor",
    )
    title = models.CharField("título", max_length=255, blank=True)
    content = models.TextField("conteúdo")
    media = models.JSONField("mídias", default=list, blank=True)
    status = models.CharField(
        "status",
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or self.content[:50]


class ScheduledPost(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        PUBLISHING = "publishing", "Publicando"
        PUBLISHED = "published", "Publicado"
        FAILED = "failed", "Falhou"
        CANCELLED = "cancelled", "Cancelado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="post",
    )
    social_account = models.ForeignKey(
        "integrations.SocialAccount",
        on_delete=models.CASCADE,
        related_name="scheduled_posts",
        verbose_name="conta social",
    )
    scheduled_at = models.DateTimeField("agendado para")
    status = models.CharField(
        "status",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    published_at = models.DateTimeField("publicado em", null=True, blank=True)
    external_post_id = models.CharField(
        "ID externo",
        max_length=255,
        blank=True,
    )
    api_response = models.JSONField("resposta da API", default=dict, blank=True)
    retry_count = models.PositiveSmallIntegerField("tentativas", default=0)
    error_message = models.TextField("mensagem de erro", blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "agendamento"
        verbose_name_plural = "agendamentos"
        ordering = ["scheduled_at"]

    def __str__(self):
        return f"{self.post} → {self.social_account} @ {self.scheduled_at}"
