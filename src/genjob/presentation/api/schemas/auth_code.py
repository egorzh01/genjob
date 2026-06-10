from __future__ import annotations

from pydantic import BaseModel

from genjob.domain.entities import AuthCodeId


class AuthCodeIdSchema(BaseModel):
    id: AuthCodeId
