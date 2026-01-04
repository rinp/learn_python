"""書籍関連のビジネスロジックを提供する service 層モジュール"""

from typing import Callable
from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions import NotFoundBookException
from app.models import Author, Book
from app.crud.book_crud import (
    delete_by_id,
    insert,
    select_all,
    select_by_id,
)
from app.schemas.param import BookCreateParam
from app.schemas.response import BookResponse


def _to_response(book: Book) -> BookResponse:
    """Book ORM オブジェクトを API レスポンスモデルに変換するヘルパー

    Args:
        book (Book): ORM の書籍オブジェクト

    Returns:
        BookResponse: API 用のレスポンスモデル
    """
    author: Author = book.author

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
    """書籍を作成する

    Args:
        session (Session): SQLAlchemy のセッション
        book_create_param (BookCreateParam): 書籍作成用の入力データ
        create_fn (Callable): 実際に DB に挿入する関数

    Returns:
        BookResponse: 作成された書籍のレスポンス DTO
    """
    with session.begin():
        book = create_fn(session, book_create_param)
        ret = _to_response(book)

    return ret


def find_one_book(
    session: Session,
    book_id: UUID,
    find_fn: Callable[[Session, UUID], Book | None] = select_by_id,
) -> BookResponse:
    """指定 ID の書籍を検索してレスポンスを返す

    Args:
        session (Session): SQLAlchemy のセッション
        book_id (UUID): 検索する書籍の ID
        find_fn (Callable): 検索を行う関数

    Returns:
        BookResponse: 検索に成功した場合のレスポンス DTO

    Raises:
        NotFoundBookException: 書籍が見つからない場合
    """
    book = find_fn(session, book_id)
    if book is None:
        raise NotFoundBookException(book_id)
    ret = _to_response(book)
    return ret


def find_all_books(
    session: Session,
    find_all_fn: Callable[[Session], list[Book]] = select_all,
) -> list[BookResponse]:
    """全ての書籍を検索してレスポンスのリストを返す

    Args:
        session (Session): SQLAlchemy のセッション
        find_all_fn (Callable): 全検索を行う関数

    Returns:
        list[BookResponse]: 検索結果のレスポンス DTO リスト
    """
    books = find_all_fn(session)
    return [_to_response(book) for book in books]


def delete_book(
    session: Session,
    book_id: UUID,
    delete_by_id_fn: Callable[[Session, UUID], bool] = delete_by_id,
) -> None:
    """指定 ID の書籍を削除する

    Args:
        session (Session): SQLAlchemy のセッション
        book_id (UUID): 削除対象の書籍 ID
        delete_by_id_fn (Callable): 実際に削除を行う関数

    Raises:
        NotFoundBookException: 削除対象の書籍が存在しない場合
    """
    with session.begin():
        is_deleted = delete_by_id_fn(session, book_id)
        if not is_deleted:
            raise NotFoundBookException(book_id)
