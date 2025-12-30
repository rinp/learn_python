from fastapi import APIRouter

router = APIRouter()

@router.get("/authors/")
def get_authers():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


@router.post("/authors/{id}")
def get_auther(id: str):
    return {"id": 1, "name": "Alice"}
