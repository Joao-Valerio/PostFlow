from typing import Any

from django.conf import settings

from .base import BaseSocialConnector, PublishResult


class TwitterConnector(BaseSocialConnector):
    platform = "twitter"

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        return (
            f"https://twitter.com/i/oauth2/authorize"
            f"?response_type=code"
            f"&client_id={settings.TWITTER_CLIENT_ID}"
            f"&redirect_uri={redirect_uri}"
            f"&scope=tweet.read+tweet.write"
            f"&state={state}"
            f"&code_challenge=challenge"
            f"&code_challenge_method=plain"
        )

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict[str, Any]:
        return {"access_token": "mock_twitter_token", "expires_in": 3600}

    def publish_post(self, content: str, media: list | None = None) -> PublishResult:
        return PublishResult(success=True, external_post_id="mock_tw_post_id")

    def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        return {"access_token": "mock_refreshed_twitter_token"}
