from app.schemas.response import BookResponse
from sqlalchemy.orm import Session
from app.schemas.param import BookCreateParam
from app.repository.book_crud import create, find_by_id, delete_by_id, select_all_with_author
import logging

def create_book(session: Session, book_create_param: BookCreateParam) -> BookResponse:
    # 書き込み系だけ transaction block を張って自動commit/rollback
    with session.begin():
        book = create(session, book_create_param)
        logging.info(f"created book: {book!r}")
        ret = BookResponse.model_validate(book)
    return ret

def find(session: Session, id: str) -> BookResponse:
    book = find_by_id(session, id)
    ret = BookResponse.model_validate(book)
    return ret

def find_all(session: Session) -> list[BookResponse]:
    return select_all_with_author(session)

def delete_book(session: Session, book_id: str) -> None:
    with session.begin():
        delete_by_id(session, book_id)
