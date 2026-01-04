from uuid import UUID

from pydantic import BaseModel, Field


class AuthorResponse(BaseModel):
    id: UUID = Field(..., description="著者の一意な識別子", example="xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx")
    name: str = Field(..., description="著者名", example="著者の氏名")


class BookResponse(BaseModel):
    class Author(BaseModel):
        id: UUID = Field(..., description="著者の一意な識別子", example="xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx")
        name: str = Field(..., description="著者名", example="著者の氏名")

    id: UUID = Field(..., description="著書の一意な識別子", example="xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx")
    title: str = Field(..., description="書籍のタイトル", example="著書の名前")
    author: Author = Field(..., description="書籍の著者情報")


class NotFoundBookResponse(BaseModel):
    message: str = Field(..., description="メッセージ", example="書籍が見つかりませんでした [id: xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx]")
    book_id: UUID = Field(..., description="書籍の一意な識別子")


class NotFoundAuthorResponse(BaseModel):
    message: str = Field(..., description="メッセージ", example="著者が見つかりませんでした [id: xxxxxxxx-xxxx-xxxx-Nxxx-xxxxxxxxxxxx]")
    author_id: UUID = Field(..., description="著者の一意な識別子")
