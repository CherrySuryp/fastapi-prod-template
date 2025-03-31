from enum import Enum
from typing import Any

from dotenv import find_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self) -> bool:
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self) -> bool:
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv(), env_file_encoding="utf-8")


class Config(CustomBaseSettings):
    ENV: Environment = Environment.PRODUCTION
    APP_NAME: str | None = None

    DATABASE_DSN: PostgresDsn
    DATABASE_POOL_SIZE: int = 16
    DATABASE_POOL_TTL: int = 60 * 20
    DATABASE_POOL_PRE_PING: bool = True

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]

    @property
    def database_dsn(self) -> str:
        return str(self.DATABASE_DSN)

    @property
    def fastapi_args(self) -> dict[str, Any]:
        app_args = {}
        if config.APP_NAME:
            app_args["title"] = self.APP_NAME

        if config.ENV.is_deployed:
            app_args["openapi_url"] = None
            app_args["docs_url"] = None
            app_args["redoc_url"] = None
        return app_args


config = Config()  # type: ignore
