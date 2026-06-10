from __future__ import annotations

from typing import TYPE_CHECKING

from genjob.application.errors import ProfileNotFoundError

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.application.interfaces import (
        IProfileRepository,
        ITransactionManager,
    )
    from genjob.domain.entities import ProfileId


class DeleteProfileUC:
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
    ) -> None:
        profile = await self._profile_repo.get_profile(
            profile_id=profile_id,
            user_id=self._auth_ctx.user_id,
        )
        if not profile:
            raise ProfileNotFoundError()

        async with self._tm.with_transaction():
            await self._profile_repo.delete_profile(profile.id)
