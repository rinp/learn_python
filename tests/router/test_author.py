import pytest

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.param import AuthorCreateParam
from app.models import Author
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from app.routers.author_router import get_create_author_service


client = TestClient(app)

@pytest.fixture(scope="function")
def override_dependency(mocker):
    def dummy_create_author_service(
        session: Session, param: AuthorCreateParam
    ):
        return Author(id=uuid4(), name=param.name)
    def get_dummy():
        return dummy_create_author_service

    mock_session:Session = mocker.MagicMock()
    def duumy_get_db():
         yield mock_session

    app.dependency_overrides[get_create_author_service] = get_dummy
    app.dependency_overrides[get_db] = duumy_get_db
    yield
    app.dependency_overrides.clear()

def test_create_author_success(override_dependency):
    response = client.post(
        "/authors",
        json={"name": "Test Author"}
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "Test Author"


def test_create_author_fail_required(override_dependency):
    response = client.post(
        "/authors",
        json={}
    )
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "Field required" # TODO

def test_create_author_fail_length(override_dependency):
    response = client.post(
        "/authors",
        json={"name": "1234567890"*5 + "1"}
    )
    data = response.json()
    assert response.status_code == 422
    assert f"{data["detail"][0]['ctx']}" == "{'max_length': 50}" # TODO

