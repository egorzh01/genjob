from __future__ import annotations

from typing import TYPE_CHECKING

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class SecurityProcessor:
    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    async def hash(self, raw: str) -> str:
        return self._hasher.hash(raw)

    async def verify(self, raw: str, hash: str) -> bool:
        try:
            return self._hasher.verify(hash, raw)
        except VerifyMismatchError:
            return False


if TYPE_CHECKING:
    from genjob.application.interfaces import ISecurityProcessor

    _: ISecurityProcessor = SecurityProcessor(*[])
