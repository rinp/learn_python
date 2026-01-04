import logging
import uuid

from pydantic import BaseModel, Field

from app.models.constants import AUTHOR_NAME_MAX_LENGTH, BOOK_TITLE_MAX_LENGTH

logger = logging.getLogger(__name__)


class AuthorCreateParam(BaseModel):
    model_config = {"extra": "forbid"}

    name: str = Field(
        ...,
        max_length=AUTHOR_NAME_MAX_LENGTH,
        description=f"著者名。最大 {AUTHOR_NAME_MAX_LENGTH} 文字。",
        example="著者の氏名",
    )


class BookCreateParam(BaseModel):
    title: str = Field(
        ...,
        max_length=BOOK_TITLE_MAX_LENGTH,
        description=f"書籍名。最大 {BOOK_TITLE_MAX_LENGTH} 文字。",
        example="著書の名前",
    )
    author_id: uuid.UUID = Field(
        ...,
        description="著者ID。既存の著者IDを指定する必要があります。",
        example="xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx",
    )
