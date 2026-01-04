import pytest
from typing import Callable, ParamSpec, TypeVar
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.routers.book_router import (
    get_find_books_service,
    get_find_book_service,
    get_create_book_service,
    get_delete_book_service,
)

from app.schemas.response import BookResponse
from app.exceptions import NotFoundBookEexception, NotFoundAuthorEexception

P = ParamSpec("P")
R = TypeVar("R")

def get_dummy(dummy_service: Callable[P, R]) -> Callable[[], Callable[P, R]]:
    def provider() -> Callable[P, R]:
        return dummy_service

    return provider


client = TestClient(app)

@pytest.fixture(scope="function")
def override_dependency(mocker):
    mock_session: Session = mocker.MagicMock()

    def dummy_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = dummy_get_db
    try:
        yield mock_session
    finally:
        app.dependency_overrides.clear()

#################################################################################
#################################################################################

def dummy_get_find_books_service(
    session: Session
) -> list[BookResponse]:
    return [
        BookResponse(id=uuid4(), title="title1", author=BookResponse.Author(id=uuid4(), name="name1")),
        BookResponse(id=uuid4(), title="title2", author=BookResponse.Author(id=uuid4(), name="name2"))
    ]

def test_find_books_success(override_dependency):
    app.dependency_overrides[get_find_books_service] = get_dummy(dummy_get_find_books_service)

    response = client.get("/books")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2

################################################################################
################################################################################
def dummy_get_find_book_service(
    session: Session, book_id: UUID
):
    return BookResponse(id=book_id, title="title", author=BookResponse.Author(id=uuid4(), name="name"))

def dummy_get_find_book_service_fail(
    session: Session, book_id: UUID
):
    raise NotFoundBookEexception(book_id=book_id)

def test_find_book_success(override_dependency):
    app.dependency_overrides[get_find_book_service] = get_dummy(dummy_get_find_book_service)

    response = client.get(f"/books/{uuid4()}")
    data = response.json()
    assert response.status_code == 200


def test_find_book_fail_unmatch(override_dependency):
    app.dependency_overrides[get_find_book_service] = get_dummy(dummy_get_find_book_service)

    response = client.get(f"/books/invalid-uuid")
    data = response.json()
    assert response.status_code == 422


def test_find_book_fail_not_found(override_dependency):
    app.dependency_overrides[get_find_book_service] = get_dummy(dummy_get_find_book_service_fail)

    response = client.get(f"/books/invalid-uuid")
    data = response.json()
    assert response.status_code == 422

#################################################################################
#################################################################################


def dummy_get_create_book_service(
    session: Session, param: BookCreateParam
):
    return BookResponse(id=uuid4(), 
                        title=param.title, 
                        author=BookResponse.Author(id=param.author_id, name="name"))

def test_create_book_success(override_dependency):
    app.dependency_overrides[get_create_book_service] = get_dummy(dummy_get_create_book_service)

    response = client.post(
        "/books",
        json={
            "title": "New Book Title",
            "author_id": str(uuid4())
        }
    )
    data = response.json()
    assert response.status_code == 201

def test_create_book_fail_title_required(override_dependency):
    app.dependency_overrides[get_create_book_service] = get_dummy(dummy_get_create_book_service)

    response = client.post(
        "/books",
        json={
            "author_id": str(uuid4())
        }
    )
    data = response.json()
    assert response.status_code == 422

def test_create_book_fail_title_required(override_dependency):
    app.dependency_overrides[get_create_book_service] = get_dummy(dummy_get_create_book_service)

    response = client.post(
        "/books",
        json={
            "title": "New Book Title",
        }
    )
    data = response.json()
    assert response.status_code == 422

def test_create_book_fail_over_length(override_dependency):
    app.dependency_overrides[get_create_book_service] = get_dummy(dummy_get_create_book_service)

    response = client.post(
        "/books",
        json={
            "title": "01234567890"*10 + "1",
            "author_id": str(uuid4())
        }
    )
    data = response.json()
    assert response.status_code == 422

def test_create_book_fail_unmatch(override_dependency):
    app.dependency_overrides[get_create_book_service] = get_dummy(dummy_get_create_book_service)

    response = client.post(
        "/books",
        json={
            "title": "New Book Title",
            "author_id": "unmatch-uuid"
        }
    )
    data = response.json()
    assert response.status_code == 422

def dummy_get_create_book_service_fail(
    session: Session, param: BookCreateParam
):
    raise NotFoundAuthorEexception(author_id=param.author_id)

def test_create_book_fail_not_found_user(override_dependency):
    app.dependency_overrides[get_create_book_service] = get_dummy(dummy_get_create_book_service_fail)

    response = client.post(
        "/books",
        json={
            "title": "New Book Title",
            "author_id": str(uuid4())
        }
    )
    data = response.json()
    assert response.status_code == 404

#################################################################################
#################################################################################


def dummy_get_delete_book_service(
    session: Session, book_id: UUID
):
    return None

def dummy_get_delete_book_service_fail(
    session: Session, book_id: UUID
):
    raise NotFoundBookEexception(book_id=book_id)


def test_delete_book_success(override_dependency):
    app.dependency_overrides[get_delete_book_service] = get_dummy(dummy_get_delete_book_service)

    response = client.delete(f"/books/{uuid4()}")
    assert response.status_code == 204

def test_delete_book_fail(override_dependency):
    app.dependency_overrides[get_delete_book_service] = get_dummy(dummy_get_delete_book_service_fail)

    response = client.delete(f"/books/{uuid4()}")
    assert response.status_code == 404


#########################################################################
#########################################################################
