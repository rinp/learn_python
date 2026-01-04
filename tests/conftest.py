import pytest

from app.models.base import Base
from app.database import engine

@pytest.fixture(scope="module")
def setup_database():
    # 前処理：全テーブルを作成
    Base.metadata.create_all(bind=engine)

    yield

    # 後処理：テーブルを全て削除
    Base.metadata.drop_all(bind=engine)
