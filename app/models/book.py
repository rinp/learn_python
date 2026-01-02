from sqlalchemy import Column, Integer, String
from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column,  relationship
from .base import Base
from .author import Author
from uuid import UUID, uuid1
from sqlalchemy import Uuid
from sqlalchemy import ForeignKey
from .constants import AUTHOR_NAME_MAX_LENGTH, BOOK_TITLE_MAX_LENGTH
from dataclasses import dataclass

@dataclass(frozen=True)
class Book(Base):
    __tablename__ = "Books"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid1)
    title: Mapped[str] = mapped_column(
        String(BOOK_TITLE_MAX_LENGTH), nullable=False)
    # 登録時には、既存の著者IDがあるが、リソースとしてNULLは許容している。
    # 現状で著者の削除もないので実質はNOT NULL扱い。
    author_id = mapped_column(ForeignKey("Authors.id"), index=True)

    author: Mapped[Author] = relationship(back_populates="books")
