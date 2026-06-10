from __future__ import annotations

from collections.abc import AsyncIterable

import asyncpg
from dishka import AnyOf, BaseScope, Component, Provider, Scope, provide
from fastapi import Request

from genjob.application.auth_context import AuthContext
from genjob.application.interfaces import (
    IAuthCodeRepository,
    ICodeGenerator,
    IProfileRepository,
    ISecurityProcessor,
    ITransactionManager,
    IUserRepository,
)
from genjob.application.usecases.add_education import AddEducationUC
from genjob.application.usecases.add_experience import AddExperienceUC
from genjob.application.usecases.create_profile import CreateProfileUC
from genjob.application.usecases.delete_education import DeleteEducationUC
from genjob.application.usecases.delete_experience import DeleteExperienceUC
from genjob.application.usecases.delete_profile import DeleteProfileUC
from genjob.application.usecases.gen_auth_code import GenAuthCodeUC
from genjob.application.usecases.update_contacts import UpdateContactsUC
from genjob.application.usecases.update_education import UpdateEducationUC
from genjob.application.usecases.update_experience import UpdateExperienceUC
from genjob.application.usecases.verify_auth_code import VerifyAuthCodeUC
from genjob.cmd.configs import ApiConfig, BaseConfig, PostgresConfig, SecurityConfig
from genjob.infrastructure.access_token_manager import AuthTokenManager
from genjob.infrastructure.code_generator import CodeGenerator, MockCodeGenerator
from genjob.infrastructure.db.repositories.auth_code import AuthCodeRepository
from genjob.infrastructure.db.repositories.profile import ProfileRepository
from genjob.infrastructure.db.repositories.user import UserRepository
from genjob.infrastructure.db.repositories.web_session import WebSessionRepository
from genjob.infrastructure.db.transaction_manager import TransactionManager
from genjob.infrastructure.security_processor import SecurityProcessor
from genjob.presentation.api.auth.auth_context_service import (
    AuthContextService,
    IAuthTokenParser,
)
from genjob.presentation.api.auth.web_session_service import (
    IWebSessionRepository,
    WebSessionService,
)
from genjob.presentation.api.presenters.current import CurrentPresenter
from genjob.presentation.api.presenters.interfaces import IProfileReadRepository
from genjob.presentation.api.presenters.profile import ProfilePresenter
from genjob.presentation.api.routers.auth import IAuthTokenCreator


class ApiConfigProvider(Provider):
    scope = Scope.APP

    def __init__(
        self,
        cfg: ApiConfig,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        super().__init__(scope, component)
        self._cfg = cfg

    @provide
    def base_cfg(self) -> BaseConfig:
        return self._cfg.base

    @provide
    def postgres_cfg(self) -> PostgresConfig:
        return self._cfg.postgres

    @provide
    def security_cfg(self) -> SecurityConfig:
        return self._cfg.security


class AsyncpgProvider(Provider):
    scope = Scope.APP

    @provide
    async def db_pool(self, cfg: PostgresConfig) -> AsyncIterable[asyncpg.Pool]:
        pool = await asyncpg.create_pool(
            dsn=str(cfg.dsn),
            min_size=10,
            max_size=40,
            command_timeout=60.0,
        )
        try:
            yield pool
        finally:
            await pool.close()

    @provide
    async def transaction_manager(
        self,
        pool: asyncpg.Pool,
    ) -> ITransactionManager:
        return TransactionManager(
            pool=pool,
        )

    @provide
    async def web_session_repo(
        self,
        pool: asyncpg.Pool,
    ) -> IWebSessionRepository:
        return WebSessionRepository(
            pool=pool,
        )

    @provide
    async def auth_code_repo(
        self,
        pool: asyncpg.Pool,
    ) -> IAuthCodeRepository:
        return AuthCodeRepository(
            pool=pool,
        )

    @provide
    async def user_repo(
        self,
        pool: asyncpg.Pool,
    ) -> IUserRepository:
        return UserRepository(
            pool=pool,
        )

    @provide
    async def profile_repo(
        self,
        pool: asyncpg.Pool,
    ) -> AnyOf[IProfileRepository, IProfileReadRepository]:
        return ProfileRepository(
            pool=pool,
        )


class ApiAuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def auth_context_service(
        self,
        request: Request,
        auth_token_parser: IAuthTokenParser,
    ) -> AuthContextService:
        return AuthContextService(
            request=request,
            auth_token_parser=auth_token_parser,
        )

    @provide
    async def web_session_service(
        self,
        web_session_repo: IWebSessionRepository,
        transaction_manager: ITransactionManager,
        security_processor: ISecurityProcessor,
    ) -> WebSessionService:
        return WebSessionService(
            transaction_manager=transaction_manager,
            web_session_repo=web_session_repo,
            security_processor=security_processor,
        )

    @provide
    async def auth_context(
        self,
        service: AuthContextService,
    ) -> AuthContext:
        return await service.get_auth_context()


class ToolsProvider(Provider):
    scope = Scope.APP

    @provide
    async def security_processor(
        self,
    ) -> ISecurityProcessor:
        return SecurityProcessor()

    @provide
    async def auth_token_manager(
        self,
        cfg: SecurityConfig,
    ) -> AnyOf[IAuthTokenCreator, IAuthTokenParser]:
        return AuthTokenManager(
            secret_key=cfg.secret_key,
        )

    @provide
    async def code_generator(self, base_cfg: BaseConfig) -> ICodeGenerator:
        if base_cfg.mode != "PROD":
            return MockCodeGenerator()
        return CodeGenerator()


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def add_education_uc(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> AddEducationUC:
        return AddEducationUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def add_experience_uc(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> AddExperienceUC:
        return AddExperienceUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def create_profile_uc(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> CreateProfileUC:
        return CreateProfileUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def delete_education_uc(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> DeleteEducationUC:
        return DeleteEducationUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def delete_experience_uc(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> DeleteExperienceUC:
        return DeleteExperienceUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def delete_profile(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> DeleteProfileUC:
        return DeleteProfileUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def gen_auth_code_uc(
        self,
        transaction_manager: ITransactionManager,
        auth_code_repo: IAuthCodeRepository,
        security_processor: ISecurityProcessor,
        code_generator: ICodeGenerator,
    ) -> GenAuthCodeUC:
        return GenAuthCodeUC(
            transaction_manager=transaction_manager,
            auth_code_repo=auth_code_repo,
            security_processor=security_processor,
            code_generator=code_generator,
        )

    @provide
    async def update_contacts_uc(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> UpdateContactsUC:
        return UpdateContactsUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def update_education_uc(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> UpdateEducationUC:
        return UpdateEducationUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def update_experience_uc(
        self,
        auth_context: AuthContext,
        transaction_manager: ITransactionManager,
        profile_repo: IProfileRepository,
    ) -> UpdateExperienceUC:
        return UpdateExperienceUC(
            auth_ctx=auth_context,
            transaction_manager=transaction_manager,
            profile_repo=profile_repo,
        )

    @provide
    async def verify_auth_code_uc(
        self,
        transaction_manager: ITransactionManager,
        auth_code_repo: IAuthCodeRepository,
        user_repo: IUserRepository,
        security_processor: ISecurityProcessor,
    ) -> VerifyAuthCodeUC:
        return VerifyAuthCodeUC(
            transaction_manager=transaction_manager,
            auth_code_repo=auth_code_repo,
            security_processor=security_processor,
            user_repo=user_repo,
        )


class PresentersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def current_presenter(
        self,
        auth_context: AuthContext,
        user_repo: IUserRepository,
    ) -> CurrentPresenter:
        return CurrentPresenter(
            auth_ctx=auth_context,
            user_repo=user_repo,
        )

    @provide
    async def profile_presenter(
        self,
        auth_ctx: AuthContext,
        profile_repo: IProfileReadRepository,
    ) -> ProfilePresenter:
        return ProfilePresenter(
            auth_ctx=auth_ctx,
            profile_repo=profile_repo,
        )
