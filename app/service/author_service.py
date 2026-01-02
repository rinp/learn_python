from app.schemas.response import AuthorResponse
from sqlalchemy.orm import Session
from app.schemas.param import AuthorParam
from app.repository.author_crud import create

def create_author(session: Session, author_param: AuthorParam) -> AuthorResponse:
    # 書き込み系だけ transaction block を張って自動commit/rollback
    with session.begin():
        author = create(session, author_param.name)
        ret = AuthorResponse.model_validate(author)
    return ret
