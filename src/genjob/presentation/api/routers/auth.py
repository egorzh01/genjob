from __future__ import annotations

import secrets
from datetime import datetime, timedelta
from typing import Annotated, Protocol

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Cookie, Header, HTTPException, Response, status

from genjob.application.usecases.gen_auth_code import (
    GenAuthCodeUC,
    GenAuthCodeUCRequest,
)
from genjob.application.usecases.verify_auth_code import (
    VerifyAuthCodeUC,
    VerifyAuthCodeUCRequest,
)
from genjob.domain.entities import AuthCodeId
from genjob.presentation.api.auth import ACCESS_TOKEN_TTL, REFRESH_TOKEN_TTL
from genjob.presentation.api.auth.auth_context_service import AuthPayload
from genjob.presentation.api.auth.web_session import WebSession, WebSessionId
from genjob.presentation.api.auth.web_session_service import WebSessionService
from genjob.presentation.api.presenters.current import CurrentPresenter
from genjob.presentation.api.schemas.auth_code import AuthCodeIdSchema
from genjob.presentation.api.schemas.token import TokenSchema
from genjob.presentation.api.schemas.user import UserSchema

router = APIRouter(
    route_class=DishkaRoute,
)
CSRF_TOKEN_HEADER_KEY = "CSRF-Token"
CSRF_TOKEN_COOKIE_KEY = "genjob_csrf_token"
REFRESH_TOKEN_COOKIE_KEY = "genjob_refresh_token"
WEB_SESSION_COOKIE_KEY = "genjob_web_session"
COOKIE_PATH = "/api/auth/token"


class IAuthTokenCreator(Protocol):
    async def create_token(
        self,
        auth_payload: AuthPayload,
        expires_at: datetime,
    ) -> str: ...


def set_auth_cookies(
    response: Response,
    web_session: WebSession,
    refresh_token: str,
    csrf_token: str,
) -> None:
    cookie_expires = web_session.updated_at + timedelta(seconds=REFRESH_TOKEN_TTL)
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_KEY,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        expires=cookie_expires,
        path=COOKIE_PATH,
    )
    response.set_cookie(
        key=WEB_SESSION_COOKIE_KEY,
        value=str(web_session.id),
        httponly=True,
        secure=True,
        samesite="lax",
        expires=cookie_expires,
        path=COOKIE_PATH,
    )
    response.set_cookie(
        key=CSRF_TOKEN_COOKIE_KEY,
        value=csrf_token,
        httponly=False,
        secure=True,
        samesite="lax",
        expires=cookie_expires,
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        key=REFRESH_TOKEN_COOKIE_KEY,
        path=COOKIE_PATH,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.delete_cookie(
        key=WEB_SESSION_COOKIE_KEY,
        path=COOKIE_PATH,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.delete_cookie(
        key=CSRF_TOKEN_COOKIE_KEY,
        path=COOKIE_PATH,
        httponly=False,
        secure=True,
        samesite="lax",
    )


@router.post(
    "/auth/codes",
    response_model=AuthCodeIdSchema,
)
async def generate_auth_code(
    uc: FromDishka[GenAuthCodeUC],
    req: GenAuthCodeUCRequest,
) -> AuthCodeIdSchema:
    auth_code_id = await uc(req)

    return AuthCodeIdSchema(
        id=auth_code_id,
    )


@router.post("/auth/codes/{auth_code_id}/verify", response_model=TokenSchema)
async def verify_auth_code(
    response: Response,
    web_session_service: FromDishka[WebSessionService],
    auth_token_creator: FromDishka[IAuthTokenCreator],
    auth_code_id: AuthCodeId,
    uc: FromDishka[VerifyAuthCodeUC],
    req: VerifyAuthCodeUCRequest,
) -> TokenSchema:
    user_id = await uc(
        auth_code_id=auth_code_id,
        req=req,
    )
    web_session, refresh_token = await web_session_service.create_web_session(user_id)
    access_token = await auth_token_creator.create_token(
        auth_payload=AuthPayload(
            user_id=user_id,
        ),
        expires_at=web_session.updated_at + timedelta(seconds=ACCESS_TOKEN_TTL),
    )
    csrf_token = secrets.token_hex(16)
    set_auth_cookies(
        response=response,
        web_session=web_session,
        refresh_token=refresh_token,
        csrf_token=csrf_token,
    )

    return TokenSchema(
        access_token=access_token,
    )


@router.post(
    "/auth/token",
    response_model=TokenSchema,
)
async def refresh_token(
    response: Response,
    web_session_service: FromDishka[WebSessionService],
    auth_token_creator: FromDishka[IAuthTokenCreator],
    refresh_token: Annotated[
        str | None,
        Cookie(validation_alias=REFRESH_TOKEN_COOKIE_KEY),
    ] = None,
    csrf_token: Annotated[
        str | None,
        Cookie(validation_alias=CSRF_TOKEN_COOKIE_KEY),
    ] = None,
    csrf_token_header: Annotated[
        str | None,
        Header(validation_alias=CSRF_TOKEN_HEADER_KEY),
    ] = None,
    web_session_id: Annotated[
        WebSessionId | None,
        Cookie(validation_alias=WEB_SESSION_COOKIE_KEY),
    ] = None,
) -> TokenSchema:
    if (
        not csrf_token
        or csrf_token != csrf_token_header
        or not web_session_id
        or not refresh_token
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED"},
        )
    web_session, new_refresh_token = await web_session_service.update_web_session(
        web_session_id=web_session_id,
        refresh_token=refresh_token,
    )
    access_token = await auth_token_creator.create_token(
        auth_payload=AuthPayload(
            user_id=web_session.user_id,
        ),
        expires_at=web_session.updated_at + timedelta(seconds=ACCESS_TOKEN_TTL),
    )
    new_csrf_token = secrets.token_hex(16)
    set_auth_cookies(
        response=response,
        web_session=web_session,
        refresh_token=new_refresh_token,
        csrf_token=new_csrf_token,
    )
    return TokenSchema(
        access_token=access_token,
    )


@router.delete("/auth/token")
async def logout(
    response: Response,
    web_session_service: FromDishka[WebSessionService],
    csrf_token: Annotated[
        str | None,
        Cookie(validation_alias=CSRF_TOKEN_COOKIE_KEY),
    ] = None,
    csrf_token_header: Annotated[
        str | None,
        Header(validation_alias=CSRF_TOKEN_HEADER_KEY),
    ] = None,
    web_session_id: Annotated[
        WebSessionId | None,
        Cookie(validation_alias=WEB_SESSION_COOKIE_KEY),
    ] = None,
) -> None:
    if csrf_token and csrf_token != csrf_token_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN"},
        )
    if web_session_id:
        try:
            await web_session_service.delete_web_session(web_session_id)
        except Exception:
            print("Failed to delete web session")

    clear_auth_cookies(response)


@router.get(
    "/auth/current",
    response_model=UserSchema,
)
async def get_current_user(
    presenter: FromDishka[CurrentPresenter],
) -> UserSchema:
    return await presenter.get_current_user()
