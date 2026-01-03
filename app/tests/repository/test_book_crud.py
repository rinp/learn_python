# from types import SimpleNamespace
# from uuid import uuid1

# from sqlalchemy.orm import Session

# from app.repository.book_crud import create


# def select_all_with_author(mocker):
#     input = "Test Author"
#     mock_session = mocker.MagicMock(spec=Session)
#     mock_author = SimpleNamespace(id=uuid1(), name=input)
#     mock_session.execute.return_value.scalar_one.return_value = mock_author

#     author = create(mock_session, input)

#     assert author.id == mock_author.id
#     assert author.name == mock_author.name
#     mock_session.execute.assert_called_once()
