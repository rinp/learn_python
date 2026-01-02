from fastapi import FastAPI, Request, Response
from app.routers import book, author
import logging

logging.basicConfig(
    level=logging.DEBUG,
    # format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    # datefmt='%Y-%m-%d %H:%M:%S'
)


logging.info("アプリが起動します")
app = FastAPI()
app.include_router(author.router)
app.include_router(book.router)

@app.middleware('http')
async def add_request_id(request: Request, call_next) -> Response:
    # ログにリクエストIDを出力
    if(request.method in ['POST']):
        log_data = (await request.json())
        logging.info(f'リクエスト: {log_data}')

    # 次のミドルウェアまたはエンドポイントを呼び出す
    response = await call_next(request)

    # レスポンスを返す
    return response

