from __future__ import annotations

from datetime import UTC, datetime
from typing import NewType
from uuid import UUID

from pydantic import BaseModel, Field
from uuid_utils import uuid7

from genjob.domain.entities import UserId

WebSessionId = NewType("WebSessionId", UUID)


class WebSession(BaseModel):
    id: WebSessionId = Field(
        frozen=True,
        default_factory=lambda: WebSessionId(UUID(str(uuid7()))),
    )
    user_id: UserId = Field(
        frozen=True,
    )
    refresh_token_hash: str = Field()
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    def update_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> None:
        self.refresh_token_hash = refresh_token_hash
        self.updated_at = datetime.now(UTC)
