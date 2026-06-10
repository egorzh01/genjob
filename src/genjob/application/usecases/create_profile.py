from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from genjob.domain.entities.profile import Profile

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.application.interfaces import (
        IProfileRepository,
        ITransactionManager,
    )
    from genjob.domain.entities import ProfileId


class CreateProfileUCRequest(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
    }
    name: str = Field(min_length=1, max_length=100)


class CreateProfileUC:
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
        req: CreateProfileUCRequest,
    ) -> ProfileId:
        profile = Profile(
            user_id=self._auth_ctx.user_id,
            name=req.name,
        )
        async with self._tm.with_transaction():
            await self._profile_repo.save_profile(profile)
        return profile.id
