from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from genjob.domain.entities.profile_experience import ProfileExperience

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.application.interfaces import (
        IProfileRepository,
        ITransactionManager,
    )
    from genjob.domain.entities import ProfileExperienceId, ProfileId


class AddExperienceUCRequest(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
    }
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


class AddExperienceUC:
    def __init__(
        self,
        auth_ctx: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> None:
        self._auth_ctx = auth_ctx
        self._tm = transaction_manager

        self._profile_repo = profile_repo

    async def __call__(
        self,
        profile_id: ProfileId,
        req: AddExperienceUCRequest,
    ) -> ProfileExperienceId:
        profile_experience = ProfileExperience(
            profile_id=profile_id,
            title=req.title,
            place=req.place,
            start_date=req.start_date,
            end_date=req.end_date,
            location=req.location,
            description=req.description,
        )

        async with self._tm.with_transaction():
            await self._profile_repo.save_profile_experience(profile_experience)
        return profile_experience.id
