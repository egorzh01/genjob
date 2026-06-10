from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from genjob.application.errors import (
    AuthCodeInvalidError,
    AuthCodeNotFoundError,
)
from genjob.domain.entities.auth_code import AUTH_CODE_TTL, TooManyAttemptsError
from genjob.domain.entities.user import User

if TYPE_CHECKING:
    from genjob.application.interfaces import (
        IAuthCodeRepository,
        ISecurityProcessor,
        ITransactionManager,
        IUserRepository,
    )
    from genjob.domain.entities import AuthCodeId, UserId


class VerifyAuthCodeUCRequest(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
    }
    code: str = Field()


class VerifyAuthCodeUC:
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        auth_code_repo: IAuthCodeRepository,
        user_repo: IUserRepository,
        security_processor: ISecurityProcessor,
    ) -> None:
        self._tm = transaction_manager
        self._security_processor = security_processor

        self._user_repo = user_repo
        self._auth_code_repo = auth_code_repo

    async def __call__(
        self,
        auth_code_id: AuthCodeId,
        req: VerifyAuthCodeUCRequest,
    ) -> UserId:
        auth_code = await self._auth_code_repo.get_auth_code(auth_code_id)
        if not auth_code:
            raise AuthCodeNotFoundError()

        if not await self._security_processor.verify(req.code, auth_code.code_hash):
            try:
                auth_code.add_attempt()
            except TooManyAttemptsError as exc:
                async with self._tm.with_transaction():
                    await self._auth_code_repo.delete_auth_code(auth_code.id)
                raise AuthCodeNotFoundError() from exc
            async with self._tm.with_transaction():
                await self._auth_code_repo.save_auth_code(auth_code)
            raise AuthCodeInvalidError()

        if datetime.now(UTC) > auth_code.created_at + timedelta(seconds=AUTH_CODE_TTL):
            async with self._tm.with_transaction():
                await self._auth_code_repo.delete_auth_code(auth_code.id)
            raise AuthCodeNotFoundError()

        async with self._tm.with_transaction():
            await self._auth_code_repo.delete_auth_code(auth_code_id=auth_code.id)
            user = await self._user_repo.get_user_by_email(auth_code.email)
            if not user:
                user = User(
                    email=auth_code.email,
                )
                await self._user_repo.save_user(user)
        return user.id
