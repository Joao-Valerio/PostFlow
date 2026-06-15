from .base import BaseSocialConnector, PublishResult
from .facebook import FacebookConnector
from .instagram import InstagramConnector
from .linkedin import LinkedInConnector
from .twitter import TwitterConnector

CONNECTOR_MAP = {
    "facebook": FacebookConnector,
    "instagram": InstagramConnector,
    "linkedin": LinkedInConnector,
    "twitter": TwitterConnector,
}


def get_connector(platform: str, access_token: str, account_id: str = "") -> BaseSocialConnector:
    connector_cls = CONNECTOR_MAP.get(platform)
    if not connector_cls:
        raise ValueError(f"Plataforma não suportada: {platform}")
    return connector_cls(access_token=access_token, account_id=account_id)
