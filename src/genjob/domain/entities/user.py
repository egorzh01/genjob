from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from uuid_utils import uuid7

from genjob.domain import BASE_MODEL_CONFIG
from genjob.domain.entities import UserId


class User(BaseModel):
    model_config = {
        **BASE_MODEL_CONFIG,
    }
    id: UserId = Field(
        frozen=True,
        default_factory=lambda: UserId(UUID(str(uuid7()))),
    )
    email: EmailStr = Field()
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
