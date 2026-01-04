import logging
from uuid import UUID

from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import delete, select
from sqlalchemy import insert as sa_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import NotFoundAuthorEexception
from app.models import Book
from app.schemas.param import BookCreateParam


def select_all(session: Session) -> list[Book]:
    stmt = select(Book)
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
    try:
        logging.info("#########################################################")
        logging.info("#########################################################")
        logging.info("#########################################################")
        logging.info("#########################################################")
        logging.info("#########################################################")
        logging.info("#########################################################")
        book = session.execute(stmt).scalar_one()
    except IntegrityError as e:
        if isinstance(e.orig, ForeignKeyViolation):
            raise NotFoundAuthorEexception(author_id=book_create_param.author_id)
    return book


def delete_by_id(session: Session, book_id: UUID) -> bool:
    stmt = delete(Book).filter(Book.id == book_id).returning(Book.id)
    result = session.execute(stmt)
    deleted_count = result.scalar_one_or_none()
    logging.info(f"Deleted count: {deleted_count}")
    return deleted_count is not None
