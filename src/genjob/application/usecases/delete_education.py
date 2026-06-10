from __future__ import annotations

from typing import TYPE_CHECKING

from genjob.application.errors import ProfileEducationNotFoundError

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.application.interfaces import (
        IProfileRepository,
        ITransactionManager,
    )
    from genjob.domain.entities import ProfileEducationId


class DeleteEducationUC:
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
    ) -> None:
        profile_education = await self._profile_repo.get_profile_education(
            profile_education_id=profile_education_id,
            user_id=self._auth_ctx.user_id,
        )
        if not profile_education:
            raise ProfileEducationNotFoundError()

        async with self._tm.with_transaction():
            await self._profile_repo.delete_profile_education(profile_education.id)
