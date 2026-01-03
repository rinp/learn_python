import logging

from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import BookNotFoundError
from app.routers import author, book
from app.schemas.response import NotFoundBookResponse

logging.basicConfig(
    level=logging.DEBUG,
    # format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    # datefmt='%Y-%m-%d %H:%M:%S'
)

#########################
logging.info("アプリが起動します")
app = FastAPI()
app.include_router(author.router, tags=["authors"])
app.include_router(book.router, tags=["books"])

logging.info(settings.database_url)


@app.exception_handler(BookNotFoundError)
async def book_not_found_handler(request: Request, exc: BookNotFoundError) -> Response:
    response = NotFoundBookResponse(
        message=str(exc),
        book_id=exc.book_id,
    )
    logging.info("####################################")
    logging.info("####################################")
    logging.info("####################################")
    logging.info("####################################")
    logging.info("####################################")
    logging.info(f"encoder: {jsonable_encoder(response)}")
    logging.info(f"dump: {response.json()}")
    # logging.info(f"dump: {json.dumps(response.dict())}")
    logging.info("####################################")
    logging.info("####################################")
    logging.info("####################################")
    logging.info("####################################")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(response),
        # content= response.json()
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
