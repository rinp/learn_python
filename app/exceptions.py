from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

@dataclass(slots=True)
class BookNotFoundError(Exception):
    book_id: UUID

    def __str__(self) -> str:
        return f"Book not found for id: {self.book_id}"
