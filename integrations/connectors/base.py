from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class PublishResult:
    success: bool
    external_post_id: str = ""
    response: dict | None = None
    error: str = ""


class BaseSocialConnector(ABC):
    """Classe abstrata para conectores de redes sociais."""

    platform: str = ""

    def __init__(self, access_token: str, account_id: str = ""):
        self.access_token = access_token
        self.account_id = account_id

    @abstractmethod
    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """Retorna a URL de autorização OAuth 2.0."""

    @abstractmethod
    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict[str, Any]:
        """Troca o código de autorização por tokens de acesso."""

    @abstractmethod
    def publish_post(self, content: str, media: list | None = None) -> PublishResult:
        """Publica conteúdo na rede social."""

    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        """Renova o token de acesso expirado."""
