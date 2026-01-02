import logging
from pydantic import BaseModel, Field, field_validator
from app.models.constants import AUTHOR_NAME_MAX_LENGTH, BOOK_TITLE_MAX_LENGTH
import uuid

logger = logging.getLogger(__name__)
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AuthorParam(BaseModel):
    # description/max_length は OpenAPI に反映され、ReDoc 上で最大文字数が表示される

    model_config = {"extra": "forbid"}
    
    name: str = Field(
        ...,
        max_length=AUTHOR_NAME_MAX_LENGTH,
        description=f"著者名。最大 {AUTHOR_NAME_MAX_LENGTH} 文字。",
        examples=["氏名"],
    )

    # @field_validator("name", mode="before")
    # @classmethod
    # def validate_name(cls, v):
    #     logger.debug("Validating author name: %r", v)
    #     if v is None:
    #         raise ValueError("著者名は必須です。")
    #     v = v.strip() if isinstance(v, str) else v
    #     if v == "":
    #         raise ValueError("著者名を入力してください。")
    #     return v

@dataclass(frozen=True, slots=True)
class BookCreateParam(BaseModel):
    title:str = Field(
        ...,
        max_length=BOOK_TITLE_MAX_LENGTH,
        description=f"書籍名。最大 {BOOK_TITLE_MAX_LENGTH} 文字。",
        examples=["本のタイトル"],
    )
    author_id:uuid.UUID = Field(
        ...,
        description="著者ID。既存の著者IDを指定してください。",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
#     新しい書籍を登録します。登録時には、既存の著者ID
# を指定する必要があります