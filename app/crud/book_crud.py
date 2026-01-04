"""書籍リポジトリ CRUD 操作を提供するモジュール"""

import logging
from uuid import UUID

from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import delete, select
from sqlalchemy import insert as sa_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import NotFoundAuthorException
from app.models import Book
from app.schemas.param import BookCreateParam


def select_all(session: Session) -> list[Book]:
    """全ての書籍を取得する

    Args:
        session (Session): SQLAlchemy のセッション

    Returns:
        list[Book]: 取得した書籍のリスト
    """
    stmt = select(Book)
    ret = session.execute(stmt).unique().scalars().all()
    return list(ret)


def select_by_id(session: Session, id: UUID) -> Book | None:
    """ID の一致する書籍を取得する

    Args:
        session (Session): SQLAlchemy のセッション
        id (UUID): 取得対象の書籍 ID

    Returns:
        Book | None: 条件に一致した書籍、見つからなければ None を返す
    """
    stmt = select(Book).filter(Book.id == id)
    return session.execute(stmt).scalar_one_or_none()


def insert(session: Session, book_create_param: BookCreateParam) -> Book:
    """書籍を登録する

    Args:
        session (Session): SQLAlchemy のセッション
        book_create_param (BookCreateParam): 書籍登録用 DTO
    Returns:
        Book: 登録された書籍 DTO

    Raises:
        NotFoundAuthorException: 指定された author_id に一致する著者が存在しない場合
    """
    stmt = (
        sa_insert(Book)
        .values(title=book_create_param.title, author_id=book_create_param.author_id)
        .returning(Book)
    )
    try:
        book = session.execute(stmt).scalar_one()
    except IntegrityError as e:
        if isinstance(e.orig, ForeignKeyViolation):
            raise NotFoundAuthorException(author_id=book_create_param.author_id)
        else:
            raise e
    return book


def delete_by_id(session: Session, book_id: UUID) -> bool:
    """指定した ID の書籍を削除する

    Args:
        session (Session): SQLAlchemy のセッション
        book_id (UUID): 削除対象の書籍 ID

    Returns:
        bool: 指定書籍の削除に成功した場合は True、それ以外は False
    """
    stmt = delete(Book).filter(Book.id == book_id).returning(Book.id)
    result = session.execute(stmt)
    deleted_count = result.scalar_one_or_none()
    logging.info(f"Deleted count: {deleted_count}")
    return deleted_count is not None
