from __future__ import annotations

import json
from typing import TYPE_CHECKING
from uuid import UUID

import pyseto
from pyseto import Key

from genjob.domain.entities import UserId
from genjob.presentation.api.auth.auth_context_service import AuthPayload

if TYPE_CHECKING:
    from datetime import datetime


class AuthTokenManager:
    def __init__(
        self,
        secret_key: str,
    ) -> None:
        self._key = Key.new(version=4, purpose="local", key=secret_key)

    async def parse(
        self,
        token: str,
    ) -> AuthPayload:
        decoded = pyseto.decode(self._key, token, deserializer=json)
        if not isinstance(decoded.payload, dict):
            raise ValueError("Invalid payload")
        return AuthPayload(
            user_id=UserId(UUID(decoded.payload["sub"])),
        )

    async def create_token(
        self,
        auth_payload: AuthPayload,
        expires_at: datetime,
    ) -> str:

        payload = {
            "sub": str(auth_payload.user_id),
            "exp": expires_at.isoformat(),
            "roles": ["user"],
        }
        return pyseto.encode(self._key, payload).decode("utf-8")


if TYPE_CHECKING:
    from genjob.presentation.api.auth.auth_context_service import IAuthTokenParser
    from genjob.presentation.api.routers.auth import IAuthTokenCreator

    _: IAuthTokenParser = AuthTokenManager(*[])
    __: IAuthTokenCreator = AuthTokenManager(*[])
