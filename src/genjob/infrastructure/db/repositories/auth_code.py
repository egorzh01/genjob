from __future__ import annotations

from typing import TYPE_CHECKING

from genjob.domain.entities.auth_code import AuthCode
from genjob.infrastructure.db import get_conn

if TYPE_CHECKING:
    import asyncpg

    from genjob.domain.entities import AuthCodeId


class AuthCodeRepository:
    def __init__(
        self,
        pool: asyncpg.Pool,
    ) -> None:
        self._pool = pool

    async def get_auth_code(self, auth_code_id: AuthCodeId) -> AuthCode | None:
        conn = get_conn(self._pool)
        row = await conn.fetchrow(
            "SELECT id, email, created_at, attempts, code_hash FROM auth_codes WHERE id = $1",
            auth_code_id,
        )
        if not row:
            return None
        return AuthCode(**row)

    async def save_auth_code(self, auth_code: AuthCode) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            """
            INSERT INTO auth_codes (id, email, created_at, attempts, code_hash)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO UPDATE SET attempts = $4
            """,
            auth_code.id,
            auth_code.email,
            auth_code.created_at,
            auth_code.attempts,
            auth_code.code_hash,
        )

    async def delete_auth_code(self, auth_code_id: AuthCodeId) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            "DELETE FROM auth_codes WHERE id = $1",
            auth_code_id,
        )


if TYPE_CHECKING:
    from genjob.application.interfaces import IAuthCodeRepository

    _: IAuthCodeRepository = AuthCodeRepository(*[])
