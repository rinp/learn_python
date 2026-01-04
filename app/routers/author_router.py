"""著者関連の API ルーター定義モジュール"""

from typing import Callable

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import app.service.author_service as service
from app.database import get_db
from app.schemas.param import AuthorCreateParam
from app.schemas.response import AuthorResponse


def get_create_author_service():
    return service.create_author


router = APIRouter()


@router.post("/authors", status_code=status.HTTP_201_CREATED)
def create_author(
    author_create_param: AuthorCreateParam,
    session: Session = Depends(get_db),
    service: Callable[[Session, AuthorCreateParam], AuthorResponse] = Depends(
        get_create_author_service
    ),
) -> AuthorResponse:
    """著者登録 API エンドポイント

    Args:
        author_create_param: 登録する著者の入力 DTO
        session: FastAPI が管理する SQLAlchemy セッション
        service: 実処理となる関数

    Returns:
        登録された著者のレスポンス DTO
    """

    return service(session, author_create_param)
