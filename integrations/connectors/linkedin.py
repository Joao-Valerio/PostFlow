from typing import Any

from django.conf import settings

from .base import BaseSocialConnector, PublishResult


class LinkedInConnector(BaseSocialConnector):
    platform = "linkedin"

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        return (
            f"https://www.linkedin.com/oauth/v2/authorization"
            f"?response_type=code"
            f"&client_id={settings.LINKEDIN_CLIENT_ID}"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
            f"&scope=w_member_social"
        )

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict[str, Any]:
        return {"access_token": "mock_linkedin_token", "expires_in": 3600}

    def publish_post(self, content: str, media: list | None = None) -> PublishResult:
        return PublishResult(success=True, external_post_id="mock_li_post_id")

    def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        return {"access_token": "mock_refreshed_linkedin_token"}
