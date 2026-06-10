from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Literal

from dishka import STRICT_VALIDATION, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.gzip import GZipMiddleware

from genjob.application.errors import AppError
from genjob.cmd.configs import ApiConfig
from genjob.cmd.dishka_providers import (
    ApiAuthProvider,
    ApiConfigProvider,
    AsyncpgProvider,
    PresentersProvider,
    ToolsProvider,
    UseCasesProvider,
)
from genjob.presentation.api.middlewares.process_time import (
    ProcessTimeMiddleware,
)
from genjob.presentation.api.routers import (
    router as api_router,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


def create_app(
    mode: Literal["DEV", "TEST", "PROD"],
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(
        _app: FastAPI,
    ) -> AsyncGenerator[None]:
        yield
        await _app.state.dishka_container.close()

    app = FastAPI(
        lifespan=lifespan,
        title="GenJob API",
        root_path="/api",
    )

    # __________________________ Exceptions __________________________ #

    @app.exception_handler(AppError)
    async def app_error_handler(
        request: Request,  # noqa: ARG001
        exc: AppError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": {
                    "code": exc.code,
                },
            },
        )

    # __________________________ Middlewares __________________________ #

    if mode != "PROD":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.add_middleware(
        ProcessTimeMiddleware,
    )
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )

    # __________________________ Routers __________________________ #
    app.include_router(
        router=api_router,
    )
    return app


def create_production_app() -> FastAPI:
    cfg = ApiConfig()
    app = create_app(
        mode=cfg.base.mode,
    )
    ioc = make_async_container(
        ApiConfigProvider(cfg),
        AsyncpgProvider(),
        ApiAuthProvider(),
        PresentersProvider(),
        ToolsProvider(),
        UseCasesProvider(),
        FastapiProvider(),
        validation_settings=STRICT_VALIDATION,
    )
    setup_dishka(ioc, app)
    return app


app = create_production_app()
