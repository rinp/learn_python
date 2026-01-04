import logging

from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import NotFoundAuthorEexception, NotFoundBookEexception
from app.routers import author_router, book_router
from app.schemas.response import NotFoundAuthorResponse, NotFoundBookResponse

logging.basicConfig(
    level=logging.DEBUG,
    # format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    # datefmt='%Y-%m-%d %H:%M:%S'
)

#########################
logging.info("アプリが起動します")
app = FastAPI()
app.include_router(author_router.router, tags=["authors"])
app.include_router(book_router.router, tags=["books"])

logging.info(settings.database_url)


@app.exception_handler(NotFoundBookEexception)
async def book_not_found_handler(
    request: Request, exc: NotFoundBookEexception
) -> Response:
    response = NotFoundBookResponse(
        message=str(exc),
        book_id=exc.book_id,
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(response),
    )


@app.exception_handler(NotFoundAuthorEexception)
async def author_not_found_handler(
    request: Request, exc: NotFoundAuthorEexception
) -> Response:
    response = NotFoundAuthorResponse(
        message=str(exc),
        author_id=exc.author_id,
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(response),
    )


@app.middleware("http")
async def add_request_id(request: Request, call_next) -> Response:
    # ログにリクエストIDを出力
    if request.method in ["POST"]:
        log_data = await request.json()
        logging.info(f"リクエスト: {log_data}")

    # 次のミドルウェアまたはエンドポイントを呼び出す
    response = await call_next(request)

    # レスポンスを返す
    return response
