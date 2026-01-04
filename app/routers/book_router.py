"""書籍関連の API ルーター定義モジュール"""

from typing import Callable
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

import app.services.book_service as service
from app.database import get_db
from app.schemas.param import BookCreateParam
from app.schemas.response import (
    BookResponse,
    NotFoundAuthorResponse,
    NotFoundBookResponse,
)

router: APIRouter = APIRouter()


def get_delete_book_service():
    return service.delete_book


def get_create_book_service():
    return service.create_book


def get_find_book_service():
    return service.find_one_book


def get_find_books_service():
    return service.find_all_books


#################################################################################
#################################################################################


@router.get("/books")
def find_books(
    session: Session = Depends(get_db),
    service: Callable[[Session], list[BookResponse]] = Depends(get_find_books_service),
) -> list[BookResponse]:
    """全件の書籍検索 API エンドポイント

    Args:
        session: FastAPI が管理する SQLAlchemy セッション
        service: 実処理となる関数

    Returns:
        すべての書籍のレスポンス DTO
    """
    return service(session)


#################################################################################
#################################################################################


@router.get(
    "/books/{book_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Book not found",
            "model": NotFoundBookResponse,
        }
    },
)
def find_book(
    book_id: UUID = Path(..., description="取得対象とする書籍の一意な識別子"),
    session: Session = Depends(get_db),
    service: Callable[[Session, UUID], BookResponse] = Depends(get_find_book_service),
) -> BookResponse:
    """idが一致する書籍検索 API エンドポイント

    Args:
        book_id: 取得対象とする書籍の一意な識別子
        session: FastAPI が管理する SQLAlchemy セッション
        service: 実処理となる関数

    Returns:
        条件に一致する書籍のレスポンス DTO
    """
    return service(session, book_id)


#################################################################################
#################################################################################


@router.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Author not found",
            "model": NotFoundAuthorResponse,
        }
    },
)
def create_book(
    book_create_param: BookCreateParam,
    session: Session = Depends(get_db),
    service: Callable[[Session, BookCreateParam], BookResponse] = Depends(
        get_create_book_service
    ),
) -> BookResponse:
    """書籍登録 API エンドポイント

    Args:
        book_create_param: 登録する書籍の入力 DTO
        session: FastAPI が管理する SQLAlchemy セッション
        service: 実処理となる関数

    Returns:
        登録された書籍のレスポンス DTO
    """
    return service(session, book_create_param)


#################################################################################
#################################################################################


@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Book not found",
            "model": NotFoundBookResponse,
        }
    },
)
def delete_book(
    book_id: UUID = Path(..., description="削除対象とする書籍の一意な識別子"),
    session: Session = Depends(get_db),
    service: Callable[[Session, UUID], None] = Depends(get_delete_book_service),
) -> None:
    """書籍削除 API エンドポイント

    Args:
        book_id: 削除対象とする書籍の一意な識別子
        session: FastAPI が管理する SQLAlchemy セッション
        service: 実処理となる関数
    """

    return service(session, book_id)


#########################################################################
#########################################################################
