from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from genjob.application.errors import ProfileEducationNotFoundError

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.application.interfaces import (
        IProfileRepository,
        ITransactionManager,
    )
    from genjob.domain.entities import ProfileEducationId


class UpdateEducationUCRequest(BaseModel):
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
    location: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    end_date: datetime | None = Field(
        default=None,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=2000,
    )


class UpdateEducationUC:
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
        profile_education_id: ProfileEducationId,
        req: UpdateEducationUCRequest,
    ) -> ProfileEducationId:
        profile_education = await self._profile_repo.get_profile_education(
            profile_education_id=profile_education_id,
            user_id=self._auth_ctx.user_id,
        )
        if not profile_education:
            raise ProfileEducationNotFoundError()
        profile_education.update(
            title=req.title or profile_education.title,
            place=req.place or profile_education.place,
            location=req.location
            if "location" in req.model_fields_set
            else profile_education.location,
            end_date=req.end_date
            if "end_date" in req.model_fields_set
            else profile_education.end_date,
            description=req.description
            if "description" in req.model_fields_set
            else profile_education.description,
        )
        async with self._tm.with_transaction():
            await self._profile_repo.save_profile_education(profile_education)
        return profile_education.id
