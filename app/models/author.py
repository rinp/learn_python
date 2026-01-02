from sqlalchemy import Column, Integer, String
from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column,  relationship
from .base import Base
# from sqlalchemy.dialects.postgresql import UUID 
from uuid import UUID, uuid1
from sqlalchemy import Uuid
from .constants import AUTHOR_NAME_MAX_LENGTH
from dataclasses import dataclass

@dataclass(frozen=True)
class Author(Base):
    __tablename__ = "Authors"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid1)
    name: Mapped[str] = mapped_column(
        String(AUTHOR_NAME_MAX_LENGTH), nullable=False)
    books: Mapped[List["Book"]] = relationship(
        back_populates="author")

