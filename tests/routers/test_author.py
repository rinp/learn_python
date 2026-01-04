"""著者ルーターのテストモジュール"""
import pytest

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.param import AuthorCreateParam
from app.models import Author
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from app.routers.author_router import get_create_author_service

from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def provider(service: Callable[P, R]) -> Callable[[], Callable[P, R]]:
    """サービス関数をrouterで利用する際に利用するプロバイダ関数

    今システムではService層の関数自体をFastAPIのDependsで提供する
    """
    def provider() -> Callable[P, R]:
        return service

    return provider

client = TestClient(app)


@pytest.fixture(scope="function")
def override_dependency(mocker):
    """DBセッションのモック化"""

    mock_session:Session = mocker.MagicMock()
    def duumy_get_db():
         yield mock_session

    app.dependency_overrides[get_db] = duumy_get_db
    yield
    app.dependency_overrides.clear()

###############################################################################
###############################################################################

def dummy_create_author_service(
    session: Session, param: AuthorCreateParam
    ):
    return Author(id=uuid4(), name=param.name)


def test_create_author_success(override_dependency):
    app.dependency_overrides[get_create_author_service] = provider(dummy_create_author_service)

    response = client.post(
        "/authors",
        json={"name": "Test Author"}
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "Test Author"



def test_create_author_fail_required(override_dependency):
    app.dependency_overrides[get_create_author_service] = provider(dummy_create_author_service)

    response = client.post(
        "/authors",
        json={}
    )
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "Field required" # TODO

def test_create_author_fail_length(override_dependency):
    app.dependency_overrides[get_create_author_service] = provider(dummy_create_author_service)

    response = client.post(
        "/authors",
        json={"name": "1234567890"*5 + "1"}
    )
    data = response.json()
    assert response.status_code == 422
    assert f"{data["detail"][0]['ctx']}" == "{'max_length': 50}" # TODO

