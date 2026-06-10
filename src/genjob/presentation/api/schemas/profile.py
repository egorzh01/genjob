from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr

from genjob.domain.entities import ProfileEducationId, ProfileExperienceId, ProfileId


class ProfileSchema(BaseModel):
    id: ProfileId
    name: str
    updated_at: datetime


class ProfileListSchema(BaseModel):
    profiles: list[ProfileSchema]


class ProfileEducationSchema(BaseModel):
    id: ProfileEducationId
    title: str
    place: str
    location: str | None
    end_date: datetime | None
    description: str | None


class ProfileEducationListSchema(BaseModel):
    educations: list[ProfileEducationSchema]


class ProfileExperienceSchema(BaseModel):
    id: ProfileExperienceId
    title: str
    place: str
    start_date: datetime | None
    end_date: datetime | None
    location: str | None
    description: str | None


class ProfileExperienceListSchema(BaseModel):
    experiences: list[ProfileExperienceSchema]


class ProfileContactsSchema(BaseModel):
    full_name: str
    email: EmailStr | None
    phone_number: str | None
    country: str | None
    city: str | None
