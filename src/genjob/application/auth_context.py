from __future__ import annotations

from pydantic import BaseModel

from genjob.domain.entities import UserId


class AuthContext(BaseModel):
    user_id: UserId
