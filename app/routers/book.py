from fastapi import APIRouter, Depends, status
from app.service.book_service import create_book as create_book_service
from app.service.book_service import delete_book as delete_book_service
from app.schemas.param import BookCreateParam
from app.schemas.response import BookResponse
from sqlalchemy.orm import Session
from app.database import get_db
import logging
from uuid import UUID

router = APIRouter()

#, response_model=schemas.User
@router.get("/books")
def get_books()-> list[BookResponse]:
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@router.get("/books/{id}")
def get_book(id: str) -> BookResponse:
    return {"id": 1, "name": "Alice"}

@router.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(
    book_create_param: BookCreateParam,
    session: Session = Depends(get_db)):

    ret = create_book_service(session, book_create_param)
    
    return ret

@router.delete("/books/{book_id}")
def delete_book(
    book_id: UUID,
    session: Session = Depends(get_db)):
    
    logging.info(f"delete book_id: {book_id!r}")
    delete_book_service(session, book_id)
    return {"message": f"delete book_id: {book_id!r}"}


