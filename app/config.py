"""アプリケーション設定を定義するモジュール"""

import os
from typing import Literal, cast

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PROFILE = os.getenv("PROFILE", "local")


class Settings(BaseSettings):
    """環境依存の値をもつクラス"""

    profile: Literal["local", "dev", "test"] = cast(
        Literal["local", "dev", "test"], ENV_PROFILE
    )
    database_url: str

    model_config = SettingsConfigDict(
        env_file=f".env.{ENV_PROFILE}",
        env_file_encoding="utf-8",
    )

    def is_dev(self) -> bool:
        """開発環境かどうかを判定する

        Returns:
            bool: 開発環境の場合は True、それ以外は False
        """
        return self.profile in ("dev", "local")


settings = Settings.model_validate({})
