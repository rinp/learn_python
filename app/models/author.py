from typing import TYPE_CHECKING, List

# from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID, uuid1

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .constants import AUTHOR_NAME_MAX_LENGTH

if TYPE_CHECKING:
    from .book import Book

class Author(Base):
    __tablename__ = "Authors"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid1)
    name: Mapped[str] = mapped_column(String(AUTHOR_NAME_MAX_LENGTH), nullable=False)

    books: Mapped[List["Book"]] = relationship(
        "Book", back_populates="author", lazy="noload"
    )
