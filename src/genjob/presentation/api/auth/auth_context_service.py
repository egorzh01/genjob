from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer

from genjob.application.auth_context import AuthContext

if TYPE_CHECKING:
    from fastapi import Request

    from genjob.domain.entities import UserId

security = HTTPBearer(
    auto_error=False,
)


@dataclass
class AuthPayload:
    user_id: UserId


class IAuthTokenParser(Protocol):
    async def parse(self, token: str) -> AuthPayload: ...


class AuthContextService:
    def __init__(
        self,
        request: Request,
        auth_token_parser: IAuthTokenParser,
    ) -> None:
        self._request = request
        self._auth_token_parser = auth_token_parser

    async def get_auth_context(
        self,
    ) -> AuthContext:
        credentials = await security(self._request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "UNAUTHORIZED"},
            )
        try:
            data = await self._auth_token_parser.parse(credentials.credentials)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "UNAUTHORIZED"},
            ) from exc
        return AuthContext(
            user_id=data.user_id,
        )
