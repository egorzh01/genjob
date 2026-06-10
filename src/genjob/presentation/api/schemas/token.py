from __future__ import annotations

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
