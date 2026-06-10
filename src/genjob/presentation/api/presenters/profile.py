from __future__ import annotations

from typing import TYPE_CHECKING

from genjob.application.errors import (
    ProfileEducationNotFoundError,
    ProfileExperienceNotFoundError,
    ProfileNotFoundError,
)
from genjob.presentation.api.schemas.profile import (
    ProfileContactsSchema,
    ProfileEducationListSchema,
    ProfileEducationSchema,
    ProfileExperienceListSchema,
    ProfileExperienceSchema,
    ProfileListSchema,
    ProfileSchema,
)

if TYPE_CHECKING:
    from genjob.application.auth_context import AuthContext
    from genjob.domain.entities import (
        ProfileEducationId,
        ProfileExperienceId,
        ProfileId,
    )
    from genjob.presentation.api.presenters.interfaces import IProfileReadRepository


class ProfilePresenter:
    def __init__(
        self,
        auth_ctx: AuthContext,
        profile_repo: IProfileReadRepository,
    ) -> None:
        self._auth_ctx = auth_ctx
        self._profile_repo = profile_repo

    async def get_profiles(self) -> ProfileListSchema:
        profiles = await self._profile_repo.get_profiles(
            user_id=self._auth_ctx.user_id,
        )
        return ProfileListSchema(
            profiles=[
                ProfileSchema(
                    id=p.id,
                    name=p.name,
                    updated_at=p.updated_at,
                )
                for p in profiles
            ],
        )

    async def get_profile(self, profile_id: ProfileId) -> ProfileSchema:
        profile = await self._profile_repo.get_profile(
            profile_id=profile_id,
            user_id=self._auth_ctx.user_id,
        )
        if not profile:
            raise ProfileNotFoundError()
        return ProfileSchema(
            id=profile.id,
            name=profile.name,
            updated_at=profile.updated_at,
        )

    async def get_profile_educations(
        self,
        profile_id: ProfileId,
    ) -> ProfileEducationListSchema:
        educations = await self._profile_repo.get_profile_educations(
            profile_id=profile_id,
            user_id=self._auth_ctx.user_id,
        )
        return ProfileEducationListSchema(
            educations=[
                ProfileEducationSchema(
                    id=e.id,
                    title=e.title,
                    place=e.place,
                    location=e.location,
                    end_date=e.end_date,
                    description=e.description,
                )
                for e in educations
            ],
        )

    async def get_profile_education(
        self,
        profile_education_id: ProfileEducationId,
    ) -> ProfileEducationSchema:
        education = await self._profile_repo.get_profile_education(
            profile_education_id=profile_education_id,
            user_id=self._auth_ctx.user_id,
        )
        if not education:
            raise ProfileEducationNotFoundError()
        return ProfileEducationSchema(
            id=education.id,
            title=education.title,
            place=education.place,
            location=education.location,
            end_date=education.end_date,
            description=education.description,
        )

    async def get_profile_experiences(
        self,
        profile_id: ProfileId,
    ) -> ProfileExperienceListSchema:
        experiences = await self._profile_repo.get_profile_experiences(
            profile_id=profile_id,
            user_id=self._auth_ctx.user_id,
        )
        return ProfileExperienceListSchema(
            experiences=[
                ProfileExperienceSchema(
                    id=e.id,
                    title=e.title,
                    place=e.place,
                    start_date=e.start_date,
                    end_date=e.end_date,
                    location=e.location,
                    description=e.description,
                )
                for e in experiences
            ],
        )

    async def get_profile_experience(
        self,
        profile_experience_id: ProfileExperienceId,
    ) -> ProfileExperienceSchema:
        experience = await self._profile_repo.get_profile_experience(
            profile_experience_id=profile_experience_id,
            user_id=self._auth_ctx.user_id,
        )
        if not experience:
            raise ProfileExperienceNotFoundError()
        return ProfileExperienceSchema(
            id=experience.id,
            title=experience.title,
            place=experience.place,
            start_date=experience.start_date,
            end_date=experience.end_date,
            location=experience.location,
            description=experience.description,
        )

    async def get_profile_contacts(
        self,
        profile_id: ProfileId,
    ) -> ProfileContactsSchema:
        contacts = await self._profile_repo.get_profile_contacts(
            profile_id=profile_id,
            user_id=self._auth_ctx.user_id,
        )
        if not contacts:
            return ProfileContactsSchema(
                full_name="",
                email=None,
                phone_number=None,
                country=None,
                city=None,
            )
        return ProfileContactsSchema(
            full_name=contacts.full_name,
            email=contacts.email,
            phone_number=contacts.phone_number,
            country=contacts.country,
            city=contacts.city,
        )
