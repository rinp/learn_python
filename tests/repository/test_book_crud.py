""""書籍のCRUDテストモジュール"""
import pytest

from app.models.base import Base
from app.models import Author, Book
from app.repository.book_crud import insert, select_all, select_by_id, delete_by_id
from app.database import engine
from app.schemas.param import BookCreateParam
from uuid import uuid4
from app.exceptions import NotFoundAuthorException
from app.database import get_db

@pytest.fixture(scope="function")
def setup_clear_db(setup_database):
    """DBの初期化
    setup_database でのテーブル生成後のfixture
    """
    db_gen = get_db()
    session = next(db_gen)

    with session.begin():
        session.query(Book).delete()
        session.query(Author).delete()
        session.add(Author(name="setup Author1"))
        session.add(Author(name="setup Author2"))

    yield session

def test_insert_success(setup_clear_db):
    session = setup_clear_db
    
    with session.begin():
        expect_author = session.query(Author).all()[0]
        ret:Book = insert(session, BookCreateParam(title="Integration Test Book", author_id=expect_author.id))

    assert ret.title == "Integration Test Book" 
    assert ret.author.id == expect_author.id
    assert ret.author.name == expect_author.name

    result = session.query(Book).all()
    assert len(result) == 1
    assert result[0].title == "Integration Test Book"
    assert result[0].author.id == expect_author.id
    assert result[0].author.name == expect_author.name

def test_insert_fail(setup_clear_db):
    session = setup_clear_db
    while True:
        uuid = uuid4()
        authors = session.query(Author).filter(Author.id == uuid).all()
        if len(authors) == 0:
            break

    with pytest.raises(NotFoundAuthorException):
        insert(session, BookCreateParam(title="Integration Test Book", author_id=uuid))
        


def test_select_all_success(setup_clear_db):
    session = setup_clear_db
    with session.begin():
        expect_authors = session.query(Author).all()
        ret1:Book = insert(session, BookCreateParam(title="Integration Test Book1", author_id=expect_authors[0].id))
        ret2:Book = insert(session, BookCreateParam(title="Integration Test Book2", author_id=expect_authors[1].id))
        ret3:Book = insert(session, BookCreateParam(title="Integration Test Book3", author_id=expect_authors[1].id))

    result = select_all(session)
    assert len(result) == 3
    result1 = list(filter(lambda b: b.id == ret1.id, result))[0]
    result2 = list(filter(lambda b: b.id == ret2.id, result))[0]
    result3 = list(filter(lambda b: b.id == ret3.id, result))[0]

    assert result1.title == "Integration Test Book1"
    assert result1.author.id == expect_authors[0].id
    assert result1.author.name == expect_authors[0].name
    assert result2.title == "Integration Test Book2"
    assert result2.author.id == expect_authors[1].id
    assert result2.author.name == expect_authors[1].name
    assert result3.title == "Integration Test Book3"
    assert result3.author.id == expect_authors[1].id
    assert result3.author.name == expect_authors[1].name

def test_select_by_id_success(setup_clear_db):
    session = setup_clear_db
    with session.begin():
        expect_authors = session.query(Author).all()
        ret1:Book = insert(session, BookCreateParam(title="Integration Test Book1", author_id=expect_authors[0].id))
        ret2:Book = insert(session, BookCreateParam(title="Integration Test Book2", author_id=expect_authors[1].id))
        ret3:Book = insert(session, BookCreateParam(title="Integration Test Book3", author_id=expect_authors[1].id))

    result = select_by_id(session, ret1.id)

    assert result.title == "Integration Test Book1"
    assert result.author.id == expect_authors[0].id
    assert result.author.name == expect_authors[0].name

def test_delete_by_id_success(setup_clear_db):
    session = setup_clear_db
    with session.begin():
        expect_authors = session.query(Author).all()
        ret1:Book = insert(session, BookCreateParam(title="Integration Test Book1", author_id=expect_authors[0].id))
        insert(session, BookCreateParam(title="Integration Test Book2", author_id=expect_authors[1].id))
        insert(session, BookCreateParam(title="Integration Test Book3", author_id=expect_authors[1].id))
        result = delete_by_id(session, ret1.id)

    assert result
    assert len(session.query(Book).all()) == 2

def test_delete_by_id_success2(setup_clear_db):
    session = setup_clear_db
    with session.begin():
        expect_authors = session.query(Author).all()
        insert(session, BookCreateParam(title="Integration Test Book1", author_id=expect_authors[0].id))
        insert(session, BookCreateParam(title="Integration Test Book2", author_id=expect_authors[1].id))
        insert(session, BookCreateParam(title="Integration Test Book3", author_id=expect_authors[1].id))
        result = delete_by_id(session, uuid4())

    assert result == False
    assert len(session.query(Book).all()) == 3
