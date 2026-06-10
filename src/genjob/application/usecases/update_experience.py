from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from genjob.application.errors import ProfileExperienceNotFoundError

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.application.interfaces import (
        IProfileRepository,
        ITransactionManager,
    )
    from genjob.domain.entities import ProfileExperienceId


class UpdateExperienceUCRequest(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
    }
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    place: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    start_date: datetime | None = Field(
        default=None,
    )
    end_date: datetime | None = Field(
        default=None,
    )
    location: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=2000,
    )


class UpdateExperienceUC:
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
        profile_experience_id: ProfileExperienceId,
        req: UpdateExperienceUCRequest,
    ) -> ProfileExperienceId:
        profile_experience = await self._profile_repo.get_profile_experience(
            profile_experience_id=profile_experience_id,
            user_id=self._auth_ctx.user_id,
        )
        if not profile_experience:
            raise ProfileExperienceNotFoundError()
        profile_experience.update(
            title=req.title or profile_experience.title,
            place=req.place or profile_experience.place,
            location=req.location
            if "location" in req.model_fields_set
            else profile_experience.location,
            start_date=req.start_date
            if "start_date" in req.model_fields_set
            else profile_experience.start_date,
            end_date=req.end_date
            if "end_date" in req.model_fields_set
            else profile_experience.end_date,
            description=req.description
            if "description" in req.model_fields_set
            else profile_experience.description,
        )
        async with self._tm.with_transaction():
            await self._profile_repo.save_profile_experience(profile_experience)
        return profile_experience.id
