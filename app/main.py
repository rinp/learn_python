from fastapi import FastAPI
from routers import auther, book

app = FastAPI()
app.include_router(auther.router)
##### app.include_router(book.router)
