from sqlalchemy import insert as sa_insert
from sqlalchemy.orm import Session

from app.models import Author


def insert(session: Session, name: str) -> Author:
    stmt = sa_insert(Author).values(name=name).returning(Author)
    author = session.execute(stmt).scalar_one()
    return author
