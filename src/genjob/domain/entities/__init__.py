from __future__ import annotations

from typing import NewType
from uuid import UUID

AuthCodeId = NewType("AuthCodeId", UUID)
UserId = NewType("UserId", UUID)
ProfileId = NewType("ProfileId", UUID)
ProfileExperienceId = NewType("ProfileExperienceId", UUID)
ProfileEducationId = NewType("ProfileEducationId", UUID)
