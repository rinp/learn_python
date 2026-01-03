# from app.repository.author_crud import create
#  = create,
from typing import Callable

from sqlalchemy.orm import Session

from app.models import Author
from app.repository.author_crud import insert
from app.schemas.param import AuthorCreateParam
from app.schemas.response import AuthorResponse


def create_author(
    session: Session,
    author_create_param: AuthorCreateParam,
    create_fn: Callable[[Session, str], Author] = insert,
) -> AuthorResponse:
    with session.begin():
        author = create_fn(session, author_create_param.name)
        ret = AuthorResponse(id=author.id, name=author.name)
    return ret
