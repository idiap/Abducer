# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Verify OIDC-issued resource tokens against a configured issuer and audience.

The deployment's authorization server owns login/PKCE and client registration.
This resource server neither accepts arbitrary bearer secrets nor trusts an
email/name supplied by a tool call. Operators provision stable subject IDs.
"""

from __future__ import annotations

import asyncio
import jwt
from mcp.server.auth.provider import AccessToken, TokenVerifier

from .config import Config
from .store import Store


class JWTVerifier(TokenVerifier):
    def __init__(self, config: Config, store: Store, key_client=None):
        self.config, self.store = config, store
        self.keys = key_client or jwt.PyJWKClient(
            config.jwks_url, cache_jwk_set=True, lifespan=300, timeout=10
        )

    def _verify(self, token: str) -> AccessToken | None:
        if not isinstance(token, str) or len(token) > 16384:
            return None
        try:
            header = jwt.get_unverified_header(token)
            if header.get("alg") not in {"RS256", "ES256"}:
                return None
            key = self.keys.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token,
                key.key,
                algorithms=["RS256", "ES256"],
                audience=self.config.audience,
                issuer=self.config.issuer,
                options={"require": ["exp", "iat", "sub", "iss", "aud"]},
            )
            subject = claims["sub"]
            if not isinstance(subject, str) or not subject:
                return None
            scope = claims.get("scope", "")
            if not isinstance(scope, str):
                return None
            scopes = scope.split()
            if self.config.required_scope not in scopes:
                return None
            self.store.profile(subject)
            return AccessToken(
                token=token,
                client_id=str(
                    claims.get("client_id", claims.get("azp", "linked-client"))
                ),
                subject=subject,
                scopes=scopes,
                expires_at=int(claims["exp"]),
                resource=self.config.audience,
                claims={"iss": self.config.issuer},
            )
        except (jwt.PyJWTError, ValueError, TypeError, KeyError, OSError):
            return None

    async def verify_token(self, token: str) -> AccessToken | None:
        # JWKS rotation can require HTTPS. Never block the ASGI event loop.
        return await asyncio.to_thread(self._verify, token)
