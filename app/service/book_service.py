from typing import Callable
from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions import BookNotFoundError
from app.models import Book
from app.repository.book_crud import (
    delete_by_id,
    insert,
    select_all_with_author,
    select_by_id,
)
from app.schemas.param import BookCreateParam
from app.schemas.response import BookResponse


def _to_response(book: Book) -> BookResponse:
    author = book.author

    return BookResponse(
        id=book.id,
        title=book.title,
        author=BookResponse.Author(id=author.id, name=author.name),
    )


def create_book(
    session: Session,
    book_create_param: BookCreateParam,
    create_fn: Callable[[Session, BookCreateParam], Book] = insert,
) -> BookResponse:
    with session.begin():
        book = create_fn(session, book_create_param)
        ret = _to_response(book)
    return ret


def find_one_book(
    session: Session,
    book_id: UUID,
    find_fn: Callable[[Session, UUID], Book | None] = select_by_id,
) -> BookResponse:
    book = find_fn(session, book_id)
    if book is None:
        raise BookNotFoundError(book_id)
    ret = _to_response(book)
    return ret


def find_all_books(
    session: Session,
    find_all_fn: Callable[[Session], list[Book]] = select_all_with_author,
) -> list[BookResponse]:
    books = find_all_fn(session)
    return [_to_response(book) for book in books]


def delete_book(
    session: Session,
    book_id: UUID,
    delete_by_id_fn: Callable[[Session, UUID], bool] = delete_by_id,
) -> None:
    with session.begin():
        is_deleted = delete_by_id_fn(session, book_id)
        if not is_deleted:
            raise BookNotFoundError(book_id)
