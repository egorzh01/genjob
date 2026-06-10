from __future__ import annotations

from typing import TYPE_CHECKING

from genjob.application.errors import UserNotFoundError
from genjob.presentation.api.schemas.user import UserSchema

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.application.interfaces import IUserRepository


class CurrentPresenter:
    def __init__(
        self,
        auth_ctx: AuthContext,
        user_repo: IUserRepository,
    ) -> None:
        self._auth_ctx = auth_ctx
        self._user_repo = user_repo

    async def get_current_user(self) -> UserSchema:
        user = await self._user_repo.get_user(self._auth_ctx.user_id)
        if not user:
            raise UserNotFoundError()
        return UserSchema(
            id=user.id,
            email=user.email,
        )
