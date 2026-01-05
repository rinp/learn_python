"""著者関連のビジネスロジックを提供する service 層モジュール"""

from typing import Callable

from sqlalchemy.orm import Session

from app.crud.author_crud import insert
from app.models import Author
from app.schemas.param import AuthorCreateParam
from app.schemas.response import AuthorResponse


def create_author(
    session: Session,
    author_create_param: AuthorCreateParam,
    create_fn: Callable[[Session, str], Author] = insert,
) -> AuthorResponse:
    """著者を作成する

    Args:
        session (Session): SQLAlchemy のセッション。
        author_create_param (AuthorCreateParam): 著者作成用の入力データ。
        create_fn (Callable): 実際に DB に挿入する関数（テストや依存注入で差し替え可能）。

    Returns:
        AuthorResponse: 作成された著者のレスポンス DTO。
    """
    with session.begin():
        author = create_fn(session, author_create_param.name)
        ret = AuthorResponse(id=author.id, name=author.name)
    return ret
