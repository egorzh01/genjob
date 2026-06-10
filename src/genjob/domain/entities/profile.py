from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, Field
from uuid_utils import uuid7

from genjob.domain import BASE_MODEL_CONFIG
from genjob.domain.entities import ProfileId, UserId


class Profile(BaseModel):
    model_config = {
        **BASE_MODEL_CONFIG,
    }
    id: ProfileId = Field(
        frozen=True,
        default_factory=lambda: ProfileId(UUID(str(uuid7()))),
    )
    user_id: UserId = Field()
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )
