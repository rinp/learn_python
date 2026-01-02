from __future__ import annotations

from typing import Optional

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.models import Author
from app.schemas.param import AuthorParam

def create(session:Session, author_name: str) -> Author:
    stmt = insert(Author).values(name=author_name).returning(Author)
    author = session.execute(stmt).one()
    return author
