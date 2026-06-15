from typing import Any

from django.conf import settings

from .base import BaseSocialConnector, PublishResult


class InstagramConnector(BaseSocialConnector):
    platform = "instagram"

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        return (
            f"https://api.instagram.com/oauth/authorize"
            f"?client_id={settings.INSTAGRAM_APP_ID}"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
            f"&scope=instagram_basic,instagram_content_publish"
            f"&response_type=code"
        )

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict[str, Any]:
        return {"access_token": "mock_instagram_token", "expires_in": 3600}

    def publish_post(self, content: str, media: list | None = None) -> PublishResult:
        return PublishResult(success=True, external_post_id="mock_ig_post_id")

    def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        return {"access_token": "mock_refreshed_instagram_token"}
