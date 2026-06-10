from __future__ import annotations

from functools import cached_property
from typing import Literal

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    mode: Literal["DEV", "TEST", "PROD"] = Field(
        default="DEV",
        validation_alias="MODE",
    )


class PostgresConfig(BaseSettings):
    host: str = Field(
        default="localhost",
        validation_alias="POSTGRES_HOST",
    )
    port: int = Field(
        default=5432,
        validation_alias="POSTGRES_PORT",
    )
    user: str = Field(
        default="postgres",
        validation_alias="POSTGRES_USER",
    )
    password: str = Field(
        default="postgres",
        validation_alias="POSTGRES_PASSWORD",
    )
    db_name: str = Field(
        default="docsbox",
        validation_alias="POSTGRES_DB",
    )

    @cached_property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}",
        )


class SecurityConfig(BaseSettings):
    secret_key: str = Field(
        default="secret_key",
        validation_alias="SECRET_KEY",
    )


class ApiConfig(BaseSettings):
    base: BaseConfig = BaseConfig()
    postgres: PostgresConfig = PostgresConfig()
    security: SecurityConfig = SecurityConfig()
