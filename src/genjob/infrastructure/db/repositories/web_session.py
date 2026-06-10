from __future__ import annotations

from typing import TYPE_CHECKING

from genjob.infrastructure.db import get_conn
from genjob.presentation.api.auth.web_session import WebSession, WebSessionId

if TYPE_CHECKING:
    import asyncpg

    from genjob.presentation.api.auth.web_session_service import IWebSessionRepository


class WebSessionRepository:
    def __init__(
        self,
        pool: asyncpg.Pool,
    ) -> None:
        self._pool = pool

    async def get_web_session(
        self,
        web_session_id: WebSessionId,
    ) -> WebSession | None:
        conn = get_conn(self._pool)
        row = await conn.fetchrow(
            """
            SELECT
                id,
                user_id,
                refresh_token_hash,
                updated_at
            FROM web_sessions
            WHERE id = $1""",
            web_session_id,
        )
        if not row:
            return None
        return WebSession(**row)

    async def save_web_session(self, web_session: WebSession) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            """
            INSERT INTO web_sessions (id, user_id, refresh_token_hash, updated_at)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (id) DO UPDATE SET refresh_token_hash = $3, updated_at = $4
            """,
            web_session.id,
            web_session.user_id,
            web_session.refresh_token_hash,
            web_session.updated_at,
        )

    async def delete_web_session(self, web_session_id: WebSessionId) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            "DELETE FROM web_sessions WHERE id = $1",
            web_session_id,
        )


if TYPE_CHECKING:
    _: IWebSessionRepository = WebSessionRepository(*[])
