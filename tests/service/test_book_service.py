import pytest

from app.exceptions import NotFoundBookEexception
from app.schemas.param import BookCreateParam
from app.schemas.response import BookResponse
from app.service.book_service import (
    create_book,
    delete_book,
    find_all_books,
    find_one_book,
)
from uuid import UUID

def test_create_book_success(mocker):
    book_id:UUID = UUID("3995be1f-dd34-4363-9a26-12bc8489b2f0")
    title = "Test Book"
    author_id:UUID = UUID("a4efc80c-5d61-43e7-b68f-740ae9a91007")
    name = "author name"

    expect_author = BookResponse.Author(id=author_id, name=name)
    expect_book = BookResponse(id=book_id, title=title, author=expect_author)

    mock_session = mocker.MagicMock()

    mock_create_fn = mocker.MagicMock()
    mock_create_fn.return_value = expect_book

    param = BookCreateParam(title=title, author_id=author_id)

    ret = create_book(
        session=mock_session, book_create_param=param, create_fn=mock_create_fn
    )

    assert ret == expect_book

    mock_create_fn.assert_called_once_with(mock_session, param)

    mock_session.begin.return_value.__enter__.assert_called_once()
    mock_session.begin.return_value.__exit__.assert_called_once()


def test_create_book_fail(mocker):
    title = "Test Book"
    author_id = UUID("a4efc80c-5d61-43e7-b68f-740ae9a91007")

    mock_session = mocker.MagicMock()

    mock_create_fn = mocker.MagicMock()
    mock_create_fn.side_effect = RuntimeError("db error")

    param = BookCreateParam(title=title, author_id=author_id)
    with pytest.raises(RuntimeError, match="db error"):
        create_book(
            session=mock_session, book_create_param=param, create_fn=mock_create_fn
        )

    mock_create_fn.assert_called_once_with(mock_session, param)

    mock_session.begin.return_value.__enter__.assert_called_once()
    mock_session.begin.return_value.__exit__.assert_called_once()


def test_find_success(mocker):
    from uuid import UUID

    book_id = UUID("3995be1f-dd34-4363-9a26-12bc8489b2f0")
    title = "Test Book"
    author_id = UUID("a4efc80c-5d61-43e7-b68f-740ae9a91007")
    name = "author name"

    expect_author = BookResponse.Author(id=author_id, name=name)
    expect_book = BookResponse(id=book_id, title=title, author=expect_author)

    mock_session = mocker.MagicMock()

    mock_find_fn = mocker.MagicMock()
    mock_find_fn.return_value = expect_book

    ret = find_one_book(session=mock_session, book_id=book_id, find_fn=mock_find_fn)
    assert ret == expect_book
    mock_find_fn.assert_called_once_with(mock_session, book_id)

    mock_session.begin.return_value.__enter__.assert_not_called()
    mock_session.begin.return_value.__exit__.assert_not_called()


def test_find_fail(mocker):
    from uuid import UUID

    book_id = UUID("3995be1f-dd34-4363-9a26-12bc8489b2f0")

    mock_session = mocker.MagicMock()

    mock_find_fn = mocker.MagicMock()
    mock_find_fn.return_value = None

    with pytest.raises(NotFoundBookEexception):
        find_one_book(session=mock_session, book_id=book_id, find_fn=mock_find_fn)

    mock_find_fn.assert_called_once_with(mock_session, book_id)

    mock_session.begin.return_value.__enter__.assert_not_called()
    mock_session.begin.return_value.__exit__.assert_not_called()


def test_find_all_success(mocker):
    book_id1 = UUID("3995be1f-dd34-4363-9a26-12bc8489b2f0")
    title1 = "Test Book"
    author_id1 = UUID("a4efc80c-5d61-43e7-b68f-740ae9a91007")
    name1 = "author name"

    book_id2 = UUID("bbf21226-9b0b-4a5b-a4e1-2f4c43c6c131")
    title2 = "Test Book 2"
    author_id2 = UUID("0701a5ea-fabd-4c65-91aa-542639cf2a8a")
    name2 = "author name 2"

    expect_author1 = BookResponse.Author(id=author_id1, name=name1)
    expect_book1 = BookResponse(id=book_id1, title=title1, author=expect_author1)

    expect_author2 = BookResponse.Author(id=author_id2, name=name2)
    expect_book2 = BookResponse(id=book_id2, title=title2, author=expect_author2)

    mock_session = mocker.MagicMock()

    mock_find_all_fn = mocker.MagicMock()
    mock_find_all_fn.return_value = [expect_book1, expect_book2]

    ret = find_all_books(session=mock_session, find_all_fn=mock_find_all_fn)
    assert ret == [expect_book1, expect_book2]
    mock_find_all_fn.assert_called_once_with(mock_session)

    mock_session.begin.return_value.__enter__.assert_not_called()
    mock_session.begin.return_value.__exit__.assert_not_called()


def test_delete_book_success(mocker):
    from uuid import UUID

    book_id = UUID("3995be1f-dd34-4363-9a26-12bc8489b2f0")

    mock_session = mocker.MagicMock()

    mock_delete_by_id_fn = mocker.MagicMock()
    mock_delete_by_id_fn.return_value = 1

    ret = delete_book(
        session=mock_session, book_id=book_id, delete_by_id_fn=mock_delete_by_id_fn
    )
    assert ret is None
    mock_delete_by_id_fn.assert_called_once_with(mock_session, book_id)

    mock_session.begin.return_value.__enter__.assert_called_once()
    mock_session.begin.return_value.__exit__.assert_called_once()


def test_delete_book_fail(mocker):
    from uuid import UUID

    book_id = UUID("3995be1f-dd34-4363-9a26-12bc8489b2f0")

    mock_session = mocker.MagicMock()

    mock_delete_by_id_fn = mocker.MagicMock()
    mock_delete_by_id_fn.return_value = 0

    with pytest.raises(NotFoundBookEexception):
        delete_book(
            session=mock_session, book_id=book_id, delete_by_id_fn=mock_delete_by_id_fn
        )
    mock_delete_by_id_fn.assert_called_once_with(mock_session, book_id)

    mock_session.begin.return_value.__enter__.assert_called_once()
    mock_session.begin.return_value.__exit__.assert_called_once()
