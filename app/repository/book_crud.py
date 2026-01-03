import logging
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy import insert as sa_insert
from sqlalchemy.orm import Session, contains_eager

from app.models import Book
from app.schemas.param import BookCreateParam


def select_all_with_author(session: Session) -> list[Book]:
    stmt = select(Book).join(Book.author).options(contains_eager(Book.author))
    ret = session.execute(stmt).unique().scalars().all()
    return list(ret)


def select_by_id(session: Session, id: UUID) -> Book | None:
    stmt = select(Book).filter(Book.id == id)
    return session.execute(stmt).scalar_one_or_none()


def insert(session: Session, book_create_param: BookCreateParam) -> Book:
    stmt = (
        sa_insert(Book)
        .values(title=book_create_param.title, author_id=book_create_param.author_id)
        .returning(Book)
    )
    book = session.execute(stmt).scalar_one()
    return book


def delete_by_id(session: Session, book_id: UUID) -> bool:
    stmt = delete(Book).filter(Book.id == book_id).returning(Book.id)
    result = session.execute(stmt)
    deleted_count = result.scalar_one_or_none()
    logging.info(f"Deleted count: {deleted_count}")
    return deleted_count is not None
