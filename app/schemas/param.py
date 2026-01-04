"""API 入力パラメータの Pydantic モデルを定義するモジュール

FastAPI の OpenAPI ドキュメントに明確な型情報としても利用します。
"""

import logging
import uuid

from pydantic import BaseModel, Field

from app.models.constants import AUTHOR_NAME_MAX_LENGTH, BOOK_TITLE_MAX_LENGTH

logger = logging.getLogger(__name__)


class AuthorCreateParam(BaseModel):
    """著者作成用の入力 DTO"""

    model_config = {"extra": "forbid"}

    name: str = Field(
        ...,
        max_length=AUTHOR_NAME_MAX_LENGTH,
        description=f"著者名。最大 {AUTHOR_NAME_MAX_LENGTH} 文字。",
        examples=["著者の氏名"],
    )


class BookCreateParam(BaseModel):
    """書籍作成用の入力 DTO"""

    model_config = {"extra": "forbid"}

    title: str = Field(
        ...,
        max_length=BOOK_TITLE_MAX_LENGTH,
        description=f"書籍名。最大 {BOOK_TITLE_MAX_LENGTH} 文字。",
        examples=["著書の名前"],
    )
    author_id: uuid.UUID = Field(
        ...,
        description="著者ID。既存の著者IDを指定する必要があります。",
        examples=["xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx"],
    )
