from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from genjob.domain.entities import (
        ProfileEducationId,
        ProfileExperienceId,
        ProfileId,
        UserId,
    )
    from genjob.domain.entities.profile import Profile
    from genjob.domain.entities.profile_education import ProfileEducation
    from genjob.domain.entities.profile_experience import ProfileExperience
    from genjob.domain.vo.profile_contacts import ProfileContacts


class IProfileReadRepository(Protocol):
    async def get_profiles(self, user_id: UserId) -> list[Profile]: ...
    async def get_profile(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> Profile | None: ...
    async def get_profile_educations(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> list[ProfileEducation]: ...
    async def get_profile_education(
        self,
        profile_education_id: ProfileEducationId,
        user_id: UserId,
    ) -> ProfileEducation | None: ...

    async def get_profile_experiences(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> list[ProfileExperience]: ...
    async def get_profile_experience(
        self,
        profile_experience_id: ProfileExperienceId,
        user_id: UserId,
    ) -> ProfileExperience | None: ...
    async def get_profile_contacts(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> ProfileContacts | None: ...
