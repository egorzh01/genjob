from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from contextlib import AbstractAsyncContextManager

    from genjob.domain.entities import (
        AuthCodeId,
        ProfileEducationId,
        ProfileExperienceId,
        ProfileId,
        UserId,
    )
    from genjob.domain.entities.auth_code import AuthCode
    from genjob.domain.entities.profile import Profile
    from genjob.domain.entities.profile_education import ProfileEducation
    from genjob.domain.entities.profile_experience import ProfileExperience
    from genjob.domain.entities.user import User
    from genjob.domain.vo.profile_contacts import ProfileContacts


class ITransactionManager(Protocol):
    def with_transaction(self) -> AbstractAsyncContextManager[None]: ...


class ISecurityProcessor(Protocol):
    async def hash(self, raw: str) -> str: ...
    async def verify(self, raw: str, hash: str) -> bool: ...


class ICodeGenerator(Protocol):
    def generate_code(self) -> str: ...


class IAuthCodeRepository(Protocol):
    async def get_auth_code(self, auth_code_id: AuthCodeId) -> AuthCode | None: ...
    async def save_auth_code(self, auth_code: AuthCode) -> None: ...
    async def delete_auth_code(self, auth_code_id: AuthCodeId) -> None: ...


class IUserRepository(Protocol):
    async def get_user(self, user_id: UserId) -> User | None: ...
    async def save_user(self, user: User) -> None: ...
    async def get_user_by_email(self, email: str) -> User | None: ...


class IProfileRepository(Protocol):
    async def get_profile(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> Profile | None: ...
    async def save_profile(self, profile: Profile) -> None: ...
    async def save_profile_experience(
        self,
        profile_experience: ProfileExperience,
    ) -> None: ...
    async def save_profile_education(
        self,
        profile_education: ProfileEducation,
    ) -> None: ...
    async def get_profile_experience(
        self,
        profile_experience_id: ProfileExperienceId,
        user_id: UserId,
    ) -> ProfileExperience | None: ...

    async def get_profile_education(
        self,
        profile_education_id: ProfileEducationId,
        user_id: UserId,
    ) -> ProfileEducation | None: ...
    async def delete_profile_education(
        self,
        profile_education_id: ProfileEducationId,
    ) -> None: ...
    async def delete_profile_experience(
        self,
        profile_experience_id: ProfileExperienceId,
    ) -> None: ...
    async def delete_profile(self, profile_id: ProfileId) -> None: ...
    async def save_profile_contacts(
        self,
        profile_id: ProfileId,
        contacts: ProfileContacts,
    ) -> None: ...
