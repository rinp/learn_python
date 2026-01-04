"""API 出力レスポンスの Pydantic モデルを定義するモジュール

FastAPI の OpenAPI ドキュメントに明確な型情報としても利用します。

"""

from uuid import UUID

from pydantic import BaseModel, Field


class AuthorResponse(BaseModel):
    """著者レスポンス DTO"""

    id: UUID = Field(
        ...,
        description="著者の一意な識別子",
        examples=["xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx"],
    )
    name: str = Field(..., description="著者名", examples=["著者の氏名"])


class BookResponse(BaseModel):
    """書籍レスポンス DTO"""

    class Author(BaseModel):
        id: UUID = Field(
            ...,
            description="著者の一意な識別子",
            examples=["xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx"],
        )
        name: str = Field(..., description="著者名", examples=["著者の氏名"])

    id: UUID = Field(
        ...,
        description="著書の一意な識別子",
        examples=["xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx"],
    )
    title: str = Field(..., description="書籍のタイトル", examples=["著書の名前"])
    author: Author = Field(..., description="書籍の著者情報")


class NotFoundBookResponse(BaseModel):
    """書籍未検出時のエラーレスポンス DTO"""

    message: str = Field(
        ...,
        description="メッセージ",
        examples=[
            "書籍が見つかりませんでした [id: xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx]"
        ],
    )
    book_id: UUID = Field(
        ...,
        description="書籍の一意な識別子",
        examples=["xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx"],
    )


class NotFoundAuthorResponse(BaseModel):
    """著者未検出時のエラーレスポンス DTO"""

    message: str = Field(
        ...,
        description="メッセージ",
        examples=[
            "著者が見つかりませんでした [id: xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx]"
        ],
    )
    author_id: UUID = Field(
        ...,
        description="著者の一意な識別子",
        examples=["xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx"],
    )
