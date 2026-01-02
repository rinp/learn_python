from fastapi import APIRouter, Depends, status
from app.service.author_service import create_author as create_author_service
from app.schemas.param import AuthorParam
from sqlalchemy.orm import Session
from app.database import get_db
import logging


router = APIRouter()

#, response_model=schemas.User
@router.get("/authors")
def get_authors():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@router.get("/authors/{id}")
def get_author(id: str):
    return {"id": 1, "name": "Alice"}

@router.post("/authors", status_code=status.HTTP_201_CREATED)
def create_author(
    author_param: AuthorParam,
    session: Session = Depends(get_db)):

    ret = create_author_service(session, author_param=author_param)
    
    return ret
#[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


