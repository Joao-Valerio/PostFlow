import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("nome", max_length=255)
    slug = models.SlugField("slug", max_length=255, unique=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "organização"
        verbose_name_plural = "organizações"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        MANAGER = "manager", "Gerente"
        CREATOR = "creator", "Criador"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="organização",
        null=True,
        blank=True,
    )
    role = models.CharField(
        "papel",
        max_length=20,
        choices=Role.choices,
        default=Role.CREATOR,
    )

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_org_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_org_manager(self):
        return self.role in (self.Role.ADMIN, self.Role.MANAGER)
