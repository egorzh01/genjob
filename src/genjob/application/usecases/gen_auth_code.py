from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr, Field

from genjob.domain.entities.auth_code import AuthCode

if TYPE_CHECKING:
    from genjob.application.interfaces import (
        IAuthCodeRepository,
        ICodeGenerator,
        ISecurityProcessor,
        ITransactionManager,
    )
    from genjob.domain.entities import AuthCodeId


class GenAuthCodeUCRequest(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
    }
    email: EmailStr = Field(
        title="User email",
    )


class GenAuthCodeUC:
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        auth_code_repo: IAuthCodeRepository,
        security_processor: ISecurityProcessor,
        code_generator: ICodeGenerator,
    ) -> None:
        self._tm = transaction_manager
        self._security_processor = security_processor
        self._code_generator = code_generator

        self._auth_code_repo = auth_code_repo

    async def __call__(
        self,
        req: GenAuthCodeUCRequest,
    ) -> AuthCodeId:
        code = self._code_generator.generate_code()
        code_hash = await self._security_processor.hash(code)
        auth_code = AuthCode(
            email=req.email,
            code_hash=code_hash,
        )
        async with self._tm.with_transaction():
            await self._auth_code_repo.save_auth_code(auth_code)
        return auth_code.id
