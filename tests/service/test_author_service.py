"""著者サービスのテストモジュール"""

from types import SimpleNamespace
from uuid import uuid1

import pytest

from app.schemas.param import AuthorCreateParam
from app.service.author_service import create_author


def test_create_author_create_success(mocker):
    name = "test"
    mock_author = SimpleNamespace(id=uuid1(), name=name)

    mock_session = mocker.MagicMock()

    mock_repo = mocker.MagicMock()
    mock_repo.create.return_value = mock_author

    param = AuthorCreateParam(name=name)

    ret = create_author(
        session=mock_session, author_create_param=param, create_fn=mock_repo.create
    )

    assert ret.id == mock_author.id
    assert ret.name == mock_author.name

    mock_repo.create.assert_called_once_with(mock_session, name)

    mock_session.begin.return_value.__enter__.assert_called_once()
    mock_session.begin.return_value.__exit__.assert_called_once()


def test_create_author_create_fail(mocker):
    name = "test"
    mock_session = mocker.MagicMock()

    mock_repo = mocker.MagicMock()
    mock_repo.create.side_effect = RuntimeError("db error")

    param = AuthorCreateParam(name=name)

    with pytest.raises(RuntimeError, match="db error"):
        create_author(
            session=mock_session, author_create_param=param, create_fn=mock_repo.create
        )

    mock_repo.create.assert_called_once_with(mock_session, name)

    mock_session.begin.return_value.__enter__.assert_called_once()
    mock_session.begin.return_value.__exit__.assert_called_once()
