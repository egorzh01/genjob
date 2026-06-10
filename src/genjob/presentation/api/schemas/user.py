from __future__ import annotations

from pydantic import BaseModel, EmailStr

from genjob.domain.entities import UserId


class UserSchema(BaseModel):
    id: UserId
    email: EmailStr
