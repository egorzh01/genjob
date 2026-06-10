from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from uuid_utils import uuid7

from genjob.domain import BASE_MODEL_CONFIG
from genjob.domain.entities import (
    ProfileEducationId,
    ProfileId,
)


class ProfileEducation(BaseModel):
    model_config = {
        **BASE_MODEL_CONFIG,
    }
    id: ProfileEducationId = Field(
        frozen=True,
        default_factory=lambda: ProfileEducationId(UUID(str(uuid7()))),
    )
    profile_id: ProfileId = Field(
        frozen=True,
    )
    title: str = Field(
        min_length=1,
        max_length=100,
    )
    place: str = Field(
        min_length=1,
        max_length=100,
    )
    location: str | None = Field(
        min_length=1,
        max_length=100,
    )
    end_date: datetime | None = Field()
    description: str | None = Field(
        min_length=1,
        max_length=2000,
    )

    def update(
        self,
        title: str,
        place: str,
        location: str | None,
        end_date: datetime | None,
        description: str | None,
    ) -> None:
        self.title = title
        self.place = place
        self.location = location
        self.end_date = end_date
        self.description = description
