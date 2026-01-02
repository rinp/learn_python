from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

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
