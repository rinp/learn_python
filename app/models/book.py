from uuid import UUID, uuid1

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .author import Author
from .base import Base
from .constants import BOOK_TITLE_MAX_LENGTH


class Book(Base):
    __tablename__ = "Books"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid1)
    title: Mapped[str] = mapped_column(String(BOOK_TITLE_MAX_LENGTH), nullable=False)
    # 登録時には、既存の著者IDがあるが、リソースとしてNULLは許容している。
    # 現状で著者の削除もないので実質はNOT NULL扱い。
    author_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("Authors.id"), index=True)

    author: Mapped[Author] = relationship(
        "Author", back_populates="books", lazy="joined"
    )
