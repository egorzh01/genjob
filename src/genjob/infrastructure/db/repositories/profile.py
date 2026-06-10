from __future__ import annotations

from typing import TYPE_CHECKING

from genjob.domain.entities.profile import Profile
from genjob.domain.entities.profile_education import ProfileEducation
from genjob.domain.entities.profile_experience import ProfileExperience
from genjob.domain.vo.profile_contacts import ProfileContacts
from genjob.infrastructure.db import get_conn

if TYPE_CHECKING:
    import asyncpg

    from genjob.domain.entities import (
        ProfileEducationId,
        ProfileExperienceId,
        ProfileId,
        UserId,
    )
    from genjob.presentation.api.presenters.interfaces import IProfileReadRepository


class ProfileRepository:
    def __init__(
        self,
        pool: asyncpg.Pool,
    ) -> None:
        self._pool = pool

    async def get_profile(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> Profile | None:
        conn = get_conn(self._pool)
        row = await conn.fetchrow(
            "SELECT id, user_id, name, updated_at FROM profiles WHERE id = $1 AND user_id = $2",
            profile_id,
            user_id,
        )
        if not row:
            return None
        return Profile(**row)

    async def save_profile(self, profile: Profile) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            """
            INSERT INTO profiles (id, user_id, name, updated_at)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (id) DO UPDATE SET name = $3
            """,
            profile.id,
            profile.user_id,
            profile.name,
            profile.updated_at,
        )

    async def delete_profile(self, profile_id: ProfileId) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            "DELETE FROM profiles WHERE id = $1",
            profile_id,
        )

    async def delete_profile_education(
        self,
        profile_education_id: ProfileEducationId,
    ) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            "DELETE FROM profile_educations WHERE id = $1",
            profile_education_id,
        )

    async def delete_profile_experience(
        self,
        profile_experience_id: ProfileExperienceId,
    ) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            "DELETE FROM profile_experiences WHERE id = $1",
            profile_experience_id,
        )

    async def get_profiles(self, user_id: UserId) -> list[Profile]:
        conn = get_conn(self._pool)
        rows = await conn.fetch(
            "SELECT id, user_id, name FROM profiles WHERE user_id = $1",
            user_id,
        )
        return [Profile(**row) for row in rows]

    async def get_profile_education(
        self,
        profile_education_id: ProfileEducationId,
        user_id: UserId,
    ) -> ProfileEducation | None:
        conn = get_conn(self._pool)
        row = await conn.fetchrow(
            """
            SELECT
                pe.id,
                pe.profile_id,
                pe.title, place,
                pe.location,
                pe.end_date,
                pe.description
            FROM profile_educations AS pe
            JOIN profiles AS p ON p.id = pe.profile_id
            WHERE pe.id = $1 AND p.user_id = $2
            """,
            profile_education_id,
            user_id,
        )
        if not row:
            return None
        return ProfileEducation(**row)

    async def get_profile_experience(
        self,
        profile_experience_id: ProfileExperienceId,
        user_id: UserId,
    ) -> ProfileExperience | None:
        conn = get_conn(self._pool)
        row = await conn.fetchrow(
            """
            SELECT
                pe.id,
                pe.profile_id,
                pe.title,
                pe.place,
                pe.start_date,
                pe.end_date,
                pe.location,
                pe.description
            FROM profile_experiences AS pe
            JOIN profiles AS p ON p.id = pe.profile_id
            WHERE pe.id = $1 AND p.user_id = $2
            """,
            profile_experience_id,
            user_id,
        )
        if not row:
            return None
        return ProfileExperience(**row)

    async def save_profile_education(
        self,
        profile_education: ProfileEducation,
    ) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            """
            INSERT INTO profile_educations (id, profile_id, title, place, location, end_date, description)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (id) DO UPDATE SET title = $3, place = $4, location = $5, end_date = $6, description = $7
            """,
            profile_education.id,
            profile_education.profile_id,
            profile_education.title,
            profile_education.place,
            profile_education.location,
            profile_education.end_date,
            profile_education.description,
        )

    async def save_profile_experience(
        self,
        profile_experience: ProfileExperience,
    ) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            """
            INSERT INTO profile_experiences (id, profile_id, title, place, start_date, end_date, location, description)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO UPDATE SET title = $3, place = $4, start_date = $5, end_date = $6, location = $7, description = $8
            """,
            profile_experience.id,
            profile_experience.profile_id,
            profile_experience.title,
            profile_experience.place,
            profile_experience.start_date,
            profile_experience.end_date,
            profile_experience.location,
            profile_experience.description,
        )

    async def save_profile_contacts(
        self,
        profile_id: ProfileId,
        contacts: ProfileContacts,
    ) -> None:
        conn = get_conn(self._pool)
        await conn.execute(
            """
            INSERT INTO profile_contacts (profile_id, full_name, email, phone_number, country, city)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (profile_id) DO UPDATE SET full_name = $2, email = $3, phone_number = $4, country = $5, city = $6
            """,
            profile_id,
            contacts.full_name,
            contacts.email,
            contacts.phone_number,
            contacts.country,
            contacts.city,
        )

    async def get_profile_contacts(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> ProfileContacts | None:
        conn = get_conn(self._pool)
        row = await conn.fetchrow(
            """
            SELECT
                profile_id,
                full_name,
                email,
                phone_number,
                country,
                city
            FROM profile_contacts AS pc
            JOIN profiles AS p ON p.id = pc.profile_id
            WHERE profile_id = $1 AND p.user_id = $2
            """,
            profile_id,
            user_id,
        )
        if not row:
            return None
        return ProfileContacts(**row)

    async def get_profile_educations(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> list[ProfileEducation]:
        conn = get_conn(self._pool)
        rows = await conn.fetch(
            """
            SELECT pe.id, pe.profile_id, pe.title, pe.place, pe.location, pe.end_date, pe.description
            FROM profile_educations AS pe
            JOIN profiles AS p ON p.id = pe.profile_id
            WHERE pe.profile_id = $1 AND p.user_id = $2
            """,
            profile_id,
            user_id,
        )
        return [ProfileEducation(**row) for row in rows]

    async def get_profile_experiences(
        self,
        profile_id: ProfileId,
        user_id: UserId,
    ) -> list[ProfileExperience]:
        conn = get_conn(self._pool)
        rows = await conn.fetch(
            """
            SELECT
                pe.id,
                pe.profile_id,
                pe.title,
                pe.place,
                pe.start_date,
                pe.end_date,
                pe.location,
                pe.description
            FROM profile_experiences AS pe
            JOIN profiles AS p ON p.id = pe.profile_id
            WHERE pe.profile_id = $1 AND p.user_id = $2
            """,
            profile_id,
            user_id,
        )
        return [ProfileExperience(**row) for row in rows]


if TYPE_CHECKING:
    from genjob.application.interfaces import IProfileRepository

    _: IProfileRepository = ProfileRepository(*[])
    _: IProfileReadRepository = ProfileRepository(*[])
