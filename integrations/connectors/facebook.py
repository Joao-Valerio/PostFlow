from typing import Any

from django.conf import settings

from .base import BaseSocialConnector, PublishResult


class FacebookConnector(BaseSocialConnector):
    platform = "facebook"

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        return (
            f"https://www.facebook.com/v19.0/dialog/oauth"
            f"?client_id={settings.FACEBOOK_APP_ID}"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
            f"&scope=pages_manage_posts,pages_read_engagement"
        )

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict[str, Any]:
        return {"access_token": "mock_facebook_token", "expires_in": 3600}

    def publish_post(self, content: str, media: list | None = None) -> PublishResult:
        return PublishResult(success=True, external_post_id="mock_fb_post_id")

    def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        return {"access_token": "mock_refreshed_facebook_token"}
