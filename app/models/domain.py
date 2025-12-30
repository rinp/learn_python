from sqlalchemy import Column, Integer, String
from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column,  relationship
from .base import Base
from sqlalchemy.dialects.postgresql import UUID 
import uuid
from sqlalchemy import Uuid
from sqlalchemy import ForeignKey

class Authors(Base):
    __tablename__ = "Authors"

    id: Mapped[Uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    name: Mapped[str] = mapped_column(
        String(50), nullable=False)
    books: Mapped[List["Book"]] = relationship(
        back_populates="author")

    def __repr__(self) -> str:
        return f"Authors(id={self.id!r}, name={self.name!r})"


class Book(Base):
    __tablename__ = "Books"

    id: Mapped[Uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    title: Mapped[str] = mapped_column(
        String(100), nullable=False)
    # 登録時には、既存の著者IDがあるが、リソースとしてNULLは許容している。
    # 現状で著者の削除もないので実質はNOT NULL扱い。
    authoer_id = mapped_column(ForeignKey("Authors.id"), index=True)

    author: Mapped[Authors] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r}, authoer_id={self.authoer_id!r})"
    