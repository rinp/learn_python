from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        # リクエスト処理中に例外が起きたら、可能ならロールバックしてセッションを綺麗にする
        db.rollback()
        raise
    finally:
        db.close()


# from sqlalchemy import text

# with engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all())
