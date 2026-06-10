from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

from genjob.domain import BASE_MODEL_CONFIG
from genjob.domain.entities import ProfileId


class ProfileContacts(BaseModel):
    model_config = {
        **BASE_MODEL_CONFIG,
    }
    profile_id: ProfileId = Field(
        frozen=True,
    )
    full_name: str = Field(
        min_length=1,
        max_length=100,
    )
    email: EmailStr | None = Field()
    phone_number: str | None = Field(
        min_length=10,
        max_length=15,
    )
    country: str | None = Field(
        min_length=1,
    )
    city: str | None = Field(
        min_length=1,
    )
