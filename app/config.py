import os
from typing import Literal, cast

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PROFILE = os.getenv("PROFILE", "local")


class Settings(BaseSettings):
    profile: Literal["local", "dev", "test"] = cast(
        Literal["local", "dev", "test"], ENV_PROFILE
    )
    database_url: str

    model_config = SettingsConfigDict(
        env_file=f".env.{ENV_PROFILE}",
        env_file_encoding="utf-8",
    )


settings = Settings.model_validate({})
