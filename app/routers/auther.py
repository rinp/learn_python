from fastapi import APIRouter

router = APIRouter()

@router.get("/authers/")
def get_authers():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


@router.post("/authers/{id}")
def get_auther(id: int):
    return {"id": 1, "name": "Alice"}
