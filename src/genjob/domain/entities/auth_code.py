from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from uuid_utils import uuid7

from genjob.domain import BASE_MODEL_CONFIG
from genjob.domain.entities import AuthCodeId

MAX_ATTEMPTS = 3
AUTH_CODE_TTL = 5 * 60


class TooManyAttemptsError(Exception):
    pass


class AuthCode(BaseModel):
    model_config = {
        **BASE_MODEL_CONFIG,
    }
    id: AuthCodeId = Field(
        frozen=True,
        default_factory=lambda: AuthCodeId(UUID(str(uuid7()))),
    )
    email: EmailStr = Field()
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
    attempts: int = Field(
        default=0,
    )
    code_hash: str = Field(
        frozen=True,
    )

    def add_attempt(self) -> None:
        if self.attempts >= MAX_ATTEMPTS:
            raise TooManyAttemptsError()
        self.attempts += 1
