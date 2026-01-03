from uuid import UUID

from pydantic import BaseModel, Field

class AuthorResponse(BaseModel):
    id: UUID = Field(..., description="著者の一意な識別子")
    name: str = Field(..., description="著者名")


class BookResponse(BaseModel):
    class Author(BaseModel):
        id: UUID = Field(..., description="著者の一意な識別子")
        name: str = Field(..., description="著者名")

    id: UUID = Field(..., description="著書の一意な識別子")
    title: str = Field(..., description="書籍のタイトル")
    author: Author = Field(..., description="書籍の著者情報")


class NotFoundBookResponse(BaseModel):
    message: str = Field(..., description="メッセージ")
    book_id: UUID = Field(..., description="書籍の一意な識別子")
