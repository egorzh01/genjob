from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import asyncpg
    from asyncpg.pool import PoolConnectionProxy

_current_conn: ContextVar[PoolConnectionProxy | None] = ContextVar(
    "current_conn",
    default=None,
)


def get_conn(pool: asyncpg.Pool) -> PoolConnectionProxy | asyncpg.Pool:
    if conn := _current_conn.get():
        return conn
    return pool
