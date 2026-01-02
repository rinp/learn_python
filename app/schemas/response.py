from typing import List
from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthorResponse:

    id: UUID
    name: str


@dataclass(frozen=True, slots=True)
class BookResponse:

    @dataclass(frozen=True, slots=True)
    class Author:
        id: UUID
        name: str

    id: UUID
    title: str
    author: Author
