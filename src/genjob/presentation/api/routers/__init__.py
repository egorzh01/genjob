from __future__ import annotations

from fastapi import APIRouter

from genjob.presentation.api.routers import auth, profile

router = APIRouter()

router.include_router(
    auth.router,
    tags=["auth"],
)
router.include_router(
    profile.router,
    tags=["profiles"],
)
