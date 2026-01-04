import pytest

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Author
from app.repository.author_crud import insert
from app.database import engine

@pytest.fixture(scope="function")
def setup_clear_db(setup_database):
    db_gen = get_db()
    session = next(db_gen)

    with session.begin():
        session.execute(delete(Author))

    try:
        yield session
    finally:
        session.rollback()
        # try:
        #     next(db_gen)
        # except StopIteration:
        #     pass

def test_insert_success(setup_clear_db):
    session = setup_clear_db
    with session.begin():
        ret:Author = insert(session, "Integration Test Author")

    assert ret.name == "Integration Test Author"

    result_authors = session.query(Author).all()
    assert len(result_authors) == 1
    assert result_authors[0].name == "Integration Test Author"
    assert result_authors[0].id == ret.id
