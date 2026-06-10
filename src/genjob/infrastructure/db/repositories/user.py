from __future__ import annotations

from typing import TYPE_CHECKING

from genjob.domain.entities.user import User
from genjob.infrastructure.db import get_conn

if TYPE_CHECKING:
    import asyncpg
    from pydantic import EmailStr

    from genjob.domain.entities import UserId


class UserRepository:
    def __init__(
        self,
        pool: asyncpg.Pool,
    ) -> None:
        self._pool = pool

    async def get_user(self, user_id: UserId) -> User | None:
        conn = get_conn(self._pool)
        row = await conn.fetchrow(
            "SELECT id, email FROM users WHERE id = $1",
            user_id,
        )
        if not row:
            return None
        return User(**row)

    async def get_user_by_email(
        self,
        email: EmailStr,
    ) -> User | None:
        conn = get_conn(self._pool)
        row = await conn.fetchrow(
            "SELECT id, email FROM users WHERE email = $1",
            email,
        )
        if not row:
            return None
        return User(**row)

    async def save_user(self, user: User) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            """
            INSERT INTO users (id, email, created_at)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
            """,
            user.id,
            user.email,
            user.created_at,
        )


if TYPE_CHECKING:
    from genjob.application.interfaces import IUserRepository

    _: IUserRepository = UserRepository(*[])
