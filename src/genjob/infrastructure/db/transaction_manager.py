from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from genjob.infrastructure.db import _current_conn

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    import asyncpg


class TransactionManager:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    @asynccontextmanager
    async def with_transaction(self) -> AsyncIterator[None]:
        async with self._pool.acquire() as conn, conn.transaction():
            token = _current_conn.set(conn)
            try:
                yield
            finally:
                _current_conn.reset(token)
