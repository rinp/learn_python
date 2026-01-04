from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class NotFoundBookEexception(Exception):
    book_id: UUID

    def __str__(self) -> str:
        return f"書籍が見つかりませんでした [id: {self.book_id}]"


@dataclass(slots=True)
class NotFoundAuthorEexception(Exception):
    author_id: UUID

    def __str__(self) -> str:
        return f"著者が見つかりませんでした [id: {self.author_id}]"
