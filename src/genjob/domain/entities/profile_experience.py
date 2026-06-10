from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from uuid_utils import uuid7

from genjob.domain import BASE_MODEL_CONFIG
from genjob.domain.entities import (
    ProfileExperienceId,
    ProfileId,
)


class ProfileExperience(BaseModel):
    model_config = {
        **BASE_MODEL_CONFIG,
    }
    id: ProfileExperienceId = Field(
        frozen=True,
        default_factory=lambda: ProfileExperienceId(UUID(str(uuid7()))),
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
    start_date: datetime | None = Field()
    end_date: datetime | None = Field()
    location: str | None = Field(
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        min_length=1,
        max_length=2000,
    )

    def update(
        self,
        title: str,
        place: str,
        start_date: datetime | None,
        end_date: datetime | None,
        location: str | None,
        description: str | None,
    ) -> None:
        self.title = title
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.description = description
