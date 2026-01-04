"""FastAPI アプリケーションのエントリポイント

FastAPI インスタンスの生成、ルーター登録、例外ハンドラや共通ミドルウェアを定義する
"""

import logging

from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import NotFoundAuthorException, NotFoundBookException
from app.routers import author_router, book_router
from app.schemas.response import NotFoundAuthorResponse, NotFoundBookResponse

logging.basicConfig(level=logging.DEBUG if settings.is_dev() else logging.INFO)

app = FastAPI()
app.include_router(author_router.router, tags=["authors"])
app.include_router(book_router.router, tags=["books"])


@app.exception_handler(NotFoundBookException)
async def book_not_found_handler(
    request: Request, exc: NotFoundBookException
) -> Response:
    """書籍の取得失敗に対するハンドラー"""
    response = NotFoundBookResponse(
        message=str(exc),
        book_id=exc.book_id,
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(response),
    )


@app.exception_handler(NotFoundAuthorException)
async def author_not_found_handler(
    request: Request, exc: NotFoundAuthorException
) -> Response:
    """著者の取得失敗に対するハンドラー"""
    response = NotFoundAuthorResponse(
        message=str(exc),
        author_id=exc.author_id,
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(response),
    )


@app.middleware("http")
async def read_request(request: Request, call_next) -> Response:
    """POST リクエストのボディをログに残しつつ処理を渡すミドルウェア"""
    if settings.is_dev() and request.method in ["POST"]:
        body_bytes = await request.body()
        if body_bytes:
            try:
                log_data = await request.json()
            except Exception:
                log_data = body_bytes.decode("utf-8", errors="replace")
            logging.debug(f"リクエスト: {log_data}")

    response = await call_next(request)

    return response
