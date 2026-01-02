from typing import Optional

from sqlalchemy import insert, delete
from sqlalchemy.orm import Session

from app.models import Book, Author
from app.schemas.param import BookCreateParam
from uuid import UUID
import logging

def select_all_with_author(session:Session)-> list[Book]:
    return session.query(Book).join(Author).all()
    
def find_by_id(session: Session, id: UUID) -> Optional[Book]:
    return session.query(Book).filter(Book.id == id).first()

def create(session:Session, book_create_param: BookCreateParam) -> Book:
    stmt = insert(Book).values(
        title=book_create_param.title,
        author_id=book_create_param.author_id).returning(Book)
    Book = session.execute(stmt).scalars().one()
    return Book

def delete_by_id(session: Session, book_id: UUID) -> None:
    stmt = delete(Book).filter(Book.id == book_id)
    ret = session.execute(stmt)
    logging.info(f"deleted rows count: {ret!r}")