from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Protocol

from fastapi import HTTPException, status

from genjob.presentation.api.auth import REFRESH_TOKEN_TTL
from genjob.presentation.api.auth.web_session import WebSession, WebSessionId

if TYPE_CHECKING:
    from genjob.application.interfaces import ISecurityProcessor, ITransactionManager
    from genjob.domain.entities import UserId


class IWebSessionRepository(Protocol):
    async def get_web_session(
        self,
        web_session_id: WebSessionId,
    ) -> WebSession | None: ...

    async def save_web_session(
        self,
        web_session: WebSession,
    ) -> None: ...

    async def delete_web_session(
        self,
        web_session_id: WebSessionId,
    ) -> None: ...


class WebSessionService:
    def __init__(
        self,
        web_session_repo: IWebSessionRepository,
        transaction_manager: ITransactionManager,
        security_processor: ISecurityProcessor,
    ) -> None:
        self._web_session_repo = web_session_repo
        self._security_processor = security_processor
        self._tm = transaction_manager

    async def create_web_session(
        self,
        user_id: UserId,
    ) -> tuple[WebSession, str]:
        refresh_token = await self._generate_refresh_token()
        refresh_token_hash = await self._security_processor.hash(refresh_token)
        web_session = WebSession(
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
        )
        async with self._tm.with_transaction():
            await self._web_session_repo.save_web_session(web_session)
        return web_session, refresh_token

    async def delete_web_session(
        self,
        web_session_id: WebSessionId,
    ) -> None:
        web_session = await self._web_session_repo.get_web_session(web_session_id)
        if not web_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "WEB_SESSION_NOT_FOUND"},
            )
        async with self._tm.with_transaction():
            await self._web_session_repo.delete_web_session(web_session_id)

    async def update_web_session(
        self,
        web_session_id: WebSessionId,
        refresh_token: str,
    ) -> tuple[WebSession, str]:
        web_session = await self._web_session_repo.get_web_session(web_session_id)
        if not web_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "WEB_SESSION_NOT_FOUND"},
            )
        if web_session.updated_at > (
            datetime.now(UTC) + timedelta(seconds=REFRESH_TOKEN_TTL)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "UNAUTHORIZED"},
            )
        if not await self._security_processor.verify(
            refresh_token,
            web_session.refresh_token_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN"},
            )
        new_refresh_token = await self._generate_refresh_token()
        new_refresh_token_hash = await self._security_processor.hash(new_refresh_token)
        web_session.update_refresh_token_hash(new_refresh_token_hash)

        async with self._tm.with_transaction():
            await self._web_session_repo.save_web_session(web_session)

        return web_session, new_refresh_token

    async def _generate_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)
