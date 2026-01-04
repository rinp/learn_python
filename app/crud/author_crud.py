"""著者リポジトリ CRUD 操作を提供するモジュール"""

from sqlalchemy import insert as sa_insert
from sqlalchemy.orm import Session

from app.models import Author


def insert(session: Session, name: str) -> Author:
    """著者を登録する

    Args:
        session (Session): SQLAlchemy のセッション
        name (str): 登録する著者の名前

    Returns:
        Author: 登録された著者 DTO
    """
    stmt = sa_insert(Author).values(name=name).returning(Author)
    author = session.execute(stmt).scalar_one()
    return author
