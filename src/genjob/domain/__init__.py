from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import ConfigDict

BASE_MODEL_CONFIG: ConfigDict = {
    "str_strip_whitespace": True,
    "extra": "forbid",
    "validate_assignment": True,
}
