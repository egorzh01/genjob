from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr, Field

from genjob.application.errors import ProfileNotFoundError
from genjob.domain.vo.profile_contacts import ProfileContacts

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.application.interfaces import (
        IProfileRepository,
        ITransactionManager,
    )
    from genjob.domain.entities import ProfileId


class UpdateContactsUCRequest(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
    }
    full_name: str = Field(
        min_length=1,
        max_length=100,
    )
    email: EmailStr | None = Field()
    phone_number: str | None = Field(
        min_length=10,
        max_length=15,
    )
    country: str | None = Field(
        min_length=1,
    )
    city: str | None = Field(
        min_length=1,
    )


class UpdateContactsUC:
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
        req: UpdateContactsUCRequest,
    ) -> None:
        profile = await self._profile_repo.get_profile(
            profile_id=profile_id,
            user_id=self._auth_ctx.user_id,
        )
        if not profile:
            raise ProfileNotFoundError()

        contacts = ProfileContacts(
            profile_id=profile.id,
            full_name=req.full_name,
            email=req.email,
            phone_number=req.phone_number,
            country=req.country,
            city=req.city,
        )
        async with self._tm.with_transaction():
            await self._profile_repo.save_profile_contacts(profile.id, contacts)
